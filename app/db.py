from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

    async def connect_to_mongodb(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.database = self.client[settings.DATABASE_NAME]

    async def close_mongodb_connection(self):
        if self.client:
            self.client.close()

db = Database()

async def get_database() -> AsyncIOMotorDatabase:
    return db.database

async def get_db() -> AsyncIOMotorDatabase:
    return db.database
