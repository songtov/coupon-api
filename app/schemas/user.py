from typing import Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.user import UserCreate, UserInDB, User


async def create_user(db: AsyncIOMotorDatabase, user: UserCreate, hashed_password: str) -> str:
    """Create a new user in the database."""
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hashed_password
    user_dict.pop("password")
    
    result = await db.users.insert_one(user_dict)
    return str(result.inserted_id)


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserInDB]:
    """Get user by ID."""
    user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
    if user_doc:
        user_doc["_id"] = str(user_doc["_id"])
        return UserInDB(**user_doc)
    return None


async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> Optional[UserInDB]:
    """Get user by email."""
    user_doc = await db.users.find_one({"email": email})
    if user_doc:
        user_doc["_id"] = str(user_doc["_id"])
        return UserInDB(**user_doc)
    return None


async def update_user(db: AsyncIOMotorDatabase, user_id: str, update_data: dict) -> bool:
    """Update user data."""
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0


async def delete_user(db: AsyncIOMotorDatabase, user_id: str) -> bool:
    """Delete user by ID."""
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0