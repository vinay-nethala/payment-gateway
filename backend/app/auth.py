from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Merchant

def get_current_merchant(
    x_api_key: str = Header(..., alias="X-Api-Key"),
    x_api_secret: str = Header(..., alias="X-Api-Secret"),
    db: Session = Depends(get_db)
) -> Merchant:
    
    # Find merchant by API Key
    merchant = db.query(Merchant).filter(Merchant.api_key == x_api_key).first()
    
    # Validate exists and secret matches
    if not merchant or merchant.api_secret != x_api_secret:
        raise HTTPException(
            status_code=401, 
            detail={
                "error": {
                    "code": "AUTHENTICATION_ERROR",
                    "description": "Invalid API credentials"
                }
            }
        )
    
    return merchant