from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import db

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

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Coupon API is running"}
