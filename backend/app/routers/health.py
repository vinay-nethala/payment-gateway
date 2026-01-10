from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    # 1. Check Database Connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        print(f"DB Error: {e}")
        db_status = "disconnected"

    # 2. Return strict JSON format required
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }