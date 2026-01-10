from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import uuid

from .database import engine, Base, SessionLocal
from .models import Merchant
from .routers import health, test_routes, orders, payments, public # <--- Added public

def seed_test_merchant():
    db = SessionLocal()
    try:
        TEST_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
        existing = db.query(Merchant).filter(Merchant.id == TEST_ID).first()
        if not existing:
            print("🌱 Seeding Test Merchant...")
            test_merchant = Merchant(
                id=TEST_ID, name="Test Merchant", email="test@example.com",
                api_key="key_test_abc123", api_secret="secret_test_xyz789", is_active=True
            )
            db.add(test_merchant)
            db.commit()
    except Exception as e:
        print(f"❌ Seeding Failed: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_test_merchant()
    yield

app = FastAPI(lifespan=lifespan)

# --- CORS (Allow Frontend to talk to Backend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify ["http://localhost:3000", "http://localhost:3001"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(test_routes.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(public.router) # <--- Register Public Router

@app.get("/")
def read_root():
    return {"message": "Payment Gateway API is ready"}