from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order, Merchant
from ..schemas import OrderCreate, OrderResponse
from ..auth import get_current_merchant
import string
import random

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

def generate_order_id():
    """Format: order_ + 16 alphanumeric chars"""
    chars = string.ascii_letters + string.digits
    random_str = ''.join(random.choices(chars, k=16))
    return f"order_{random_str}"

@router.post("", response_model=OrderResponse, status_code=201)
def create_order(
    order_data: OrderCreate,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # 1. Generate Unique ID
    new_id = generate_order_id()
    while db.query(Order).filter(Order.id == new_id).first():
        new_id = generate_order_id() # Retry if collision (rare)

    # 2. Create Order Record
    new_order = Order(
        id=new_id,
        merchant_id=merchant.id,
        amount=order_data.amount,
        currency=order_data.currency,
        receipt=order_data.receipt,
        notes=order_data.notes,
        status="created"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return new_order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    # Fetch order and ensure it belongs to the authenticated merchant
    order = db.query(Order).filter(
        Order.id == order_id, 
        Order.merchant_id == merchant.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND_ERROR",
                    "description": "Order not found"
                }
            }
        )
        
    return order