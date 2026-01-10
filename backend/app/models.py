from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    api_key = Column(String(64), nullable=False, unique=True)
    api_secret = Column(String(64), nullable=False)
    webhook_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(64), primary_key=True) # Format: order_ + 16 chars
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False, index=True)
    amount = Column(Integer, nullable=False) # Minimum 100
    currency = Column(String(3), default='INR')
    receipt = Column(String(255), nullable=True)
    notes = Column(JSON, nullable=True)
    status = Column(String(20), default='created')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('amount >= 100', name='check_min_amount'),
    )

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(64), primary_key=True) # Format: pay_ + 16 chars
    order_id = Column(String(64), ForeignKey("orders.id"), nullable=False, index=True)
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), default='INR')
    method = Column(String(20), nullable=False) # upi or card
    status = Column(String(20), default='created', index=True) # Logic will set this to 'processing'
    vpa = Column(String(255), nullable=True)
    card_network = Column(String(20), nullable=True)
    card_last4 = Column(String(4), nullable=True)
    error_code = Column(String(50), nullable=True)
    error_description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())