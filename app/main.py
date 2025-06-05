from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import db
from app.api.auth import router as auth_router
from app.api.company import router as company_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect_to_mongodb()
    yield
    # Shutdown
    await db.close_mongodb_connection()

app = FastAPI(
    title="Coupon API",
    description="A FastAPI-based coupon management system for cafes",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(company_router, prefix="/api/companies", tags=["Companies"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Coupon API is running"}
