from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None

    async def connect_to_mongodb(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)

    async def close_mongodb_connection(self):
        if self.client:
            self.client.close()

db = Database()
