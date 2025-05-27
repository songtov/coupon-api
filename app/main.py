from fastapi import FastAPI
from app.db import db

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await db.connect_to_mongodb()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_mongodb_connection()

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
