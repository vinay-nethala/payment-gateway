from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order, Payment, Merchant
from ..schemas import OrderResponse, PaymentCreate, PaymentResponse
from ..utils import validate_vpa, validate_luhn, get_card_network, validate_expiry
from .payments import create_payment # Reuse logic if possible, or reimplement slightly
import string
import random
import asyncio
import os

router = APIRouter(prefix="/api/v1/public", tags=["Public Checkout"])

# Public Endpoint to fetch Order Details (No Auth needed)
@router.get("/orders/{order_id}")
def get_public_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Return minimal info needed for checkout
    return {
        "id": order.id,
        "amount": order.amount,
        "currency": order.currency,
        "status": order.status,
        "merchant_name": "Test Merchant" # In real app, join with Merchant table
    }

# Public Endpoint to Process Payment (No Auth needed, but validated by Order ID)
@router.post("/payments")
async def create_public_payment(pay_data: PaymentCreate, db: Session = Depends(get_db)):
    # 1. Fetch Order
    order = db.query(Order).filter(Order.id == pay_data.order_id).first()
    if not order:
         raise HTTPException(status_code=404, detail="Order not found")
         
    # 2. Re-use the Merchant from the Order
    merchant = db.query(Merchant).filter(Merchant.id == order.merchant_id).first()
    
    # 3. Call the logic directly (re-implementing briefly to avoid dependency circles)
    # Validate
    card_network = None
    card_last4 = None
    
    if pay_data.method == "upi":
        if not pay_data.vpa or not validate_vpa(pay_data.vpa):
            raise HTTPException(status_code=400, detail="Invalid VPA")
    elif pay_data.method == "card":
        if not pay_data.card or not validate_luhn(pay_data.card.number):
             raise HTTPException(status_code=400, detail="Invalid Card")
        card_network = get_card_network(pay_data.card.number)
        card_last4 = pay_data.card.number[-4:]

    # Create Payment Record
    chars = string.ascii_letters + string.digits
    new_id = f"pay_{''.join(random.choices(chars, k=16))}"
    
    new_payment = Payment(
        id=new_id,
        order_id=order.id,
        merchant_id=merchant.id,
        amount=order.amount,
        currency=order.currency,
        method=pay_data.method,
        status="processing",
        vpa=pay_data.vpa,
        card_network=card_network,
        card_last4=card_last4
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    
    # Simulation (Async)
    is_test = os.getenv("TEST_MODE", "false").lower() == "true"
    if is_test:
        await asyncio.sleep(int(os.getenv("TEST_PROCESSING_DELAY", "1000")) / 1000)
        success = os.getenv("TEST_PAYMENT_SUCCESS", "true").lower() == "true"
    else:
        await asyncio.sleep(random.uniform(5, 8))
        success = random.random() < (0.90 if pay_data.method == "upi" else 0.95)
        
    new_payment.status = "success" if success else "failed"
    if not success:
        new_payment.error_code = "PAYMENT_FAILED"
        new_payment.error_description = "Declined"
        
    db.commit()
    db.refresh(new_payment)
    return new_payment
    
# Public Status Check
@router.get("/payments/{payment_id}")
def get_public_payment_status(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
         raise HTTPException(status_code=404, detail="Payment not found")
    return payment