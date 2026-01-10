from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Payment, Order, Merchant
from ..schemas import PaymentCreate, PaymentResponse
from ..auth import get_current_merchant
from ..utils import validate_vpa, validate_luhn, get_card_network, validate_expiry
from typing import List
import string
import random
import asyncio
import os
import re

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

# Generate Payment ID
def generate_pay_id():
    chars = string.ascii_letters + string.digits
    random_str = ''.join(random.choices(chars, k=16))
    return f"pay_{random_str}"

@router.post("", response_model=PaymentResponse, status_code=201)
async def create_payment(
    pay_data: PaymentCreate,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # 1. Verify Order exists & belongs to merchant
    order = db.query(Order).filter(Order.id == pay_data.order_id, Order.merchant_id == merchant.id).first()
    if not order:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND_ERROR", "description": "Order not found"}})

    # 2. Validate Inputs
    card_network = None
    card_last4 = None
    
    if pay_data.method == "upi":
        if not pay_data.vpa or not validate_vpa(pay_data.vpa):
            raise HTTPException(status_code=400, detail={"error": {"code": "INVALID_VPA", "description": "Invalid VPA format"}})
            
    elif pay_data.method == "card":
        if not pay_data.card:
            raise HTTPException(status_code=400, detail={"error": {"code": "BAD_REQUEST_ERROR", "description": "Card details required"}})
        
        # Luhn Check
        if not validate_luhn(pay_data.card.number):
             raise HTTPException(status_code=400, detail={"error": {"code": "INVALID_CARD", "description": "Invalid card number"}})
        
        # Expiry Check
        if not validate_expiry(pay_data.card.expiry_month, pay_data.card.expiry_year):
             raise HTTPException(status_code=400, detail={"error": {"code": "EXPIRED_CARD", "description": "Card expired"}})
             
        card_network = get_card_network(pay_data.card.number)
        card_last4 = pay_data.card.number[-4:]

    # 3. Create Payment (Status: Processing)
    new_id = generate_pay_id()
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
    
    # 4. Simulate Bank Delay (Async)
    # Check Test Mode
    is_test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
    
    if is_test_mode:
        delay_ms = int(os.getenv("TEST_PROCESSING_DELAY", "1000"))
        await asyncio.sleep(delay_ms / 1000)
        
        # Force success/fail based on ENV
        success = os.getenv("TEST_PAYMENT_SUCCESS", "true").lower() == "true"
    else:
        # Random Delay 5-10s
        delay = random.uniform(5, 10)
        await asyncio.sleep(delay)
        
        # Random Success (90% UPI, 95% Card)
        if pay_data.method == "upi":
            success = random.random() < 0.90
        else:
            success = random.random() < 0.95

    # 5. Update Status
    if success:
        new_payment.status = "success"
    else:
        new_payment.status = "failed"
        new_payment.error_code = "PAYMENT_FAILED"
        new_payment.error_description = "Bank declined transaction"
        
    db.commit()
    db.refresh(new_payment)
    
    return new_payment

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: str,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(Payment.id == payment_id, Payment.merchant_id == merchant.id).first()
    
    if not payment:
         raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND_ERROR", "description": "Payment not found"}})
         
    return payment

@router.get("", response_model=List[PaymentResponse])
def list_payments(
    skip: int = 0, 
    limit: int = 100,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    payments = db.query(Payment).filter(
        Payment.merchant_id == merchant.id
    ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    
    return payments