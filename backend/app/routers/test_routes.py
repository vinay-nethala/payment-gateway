from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Merchant
import uuid

router = APIRouter(prefix="/api/v1/test", tags=["Test"])

@router.get("/merchant")
def get_test_merchant(db: Session = Depends(get_db)):
    # Exact UUID required by the challenge
    test_id = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
    
    merchant = db.query(Merchant).filter(Merchant.id == test_id).first()
    
    if not merchant:
        raise HTTPException(status_code=404, detail="Test merchant not found")
        
    return {
        "id": str(merchant.id),
        "email": merchant.email,
        "api_key": merchant.api_key,
        "seeded": True
    }