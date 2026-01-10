from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

# --- Order Schemas ---
class OrderCreate(BaseModel):
    amount: int = Field(..., ge=100, description="Amount in paise (min 100)")
    currency: str = Field("INR", max_length=3)
    receipt: Optional[str] = Field(None, max_length=255)
    notes: Optional[Dict[str, Any]] = None

class OrderResponse(BaseModel):
    id: str
    merchant_id: uuid.UUID
    amount: int
    currency: str
    receipt: Optional[str]
    notes: Optional[Dict[str, Any]]
    status: str
    created_at: datetime
    updated_at: datetime

  # ... existing Order schemas ...

# --- Payment Schemas ---
class CardDetails(BaseModel):
    number: str
    expiry_month: str
    expiry_year: str
    cvv: str
    holder_name: str

class PaymentCreate(BaseModel):
    order_id: str
    method: str = Field(..., pattern="^(upi|card)$")
    vpa: Optional[str] = None
    card: Optional[CardDetails] = None

class PaymentResponse(BaseModel):
    id: str
    order_id: str
    amount: int
    currency: str
    method: str
    status: str
    vpa: Optional[str]
    card_network: Optional[str]
    card_last4: Optional[str]
    error_code: Optional[str]
    error_description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True