from typing import Optional, List
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.coupon import CouponCreate, CouponInDB, Coupon


async def create_coupon(db: AsyncIOMotorDatabase, coupon: CouponCreate, client_id: str) -> str:
    """Create a new coupon in the database."""
    coupon_dict = coupon.model_dump()
    coupon_dict["client_id"] = client_id
    coupon_dict["count"] = 0
    coupon_dict["created_at"] = datetime.now(timezone.utc)
    coupon_dict["updated_at"] = datetime.now(timezone.utc)
    
    result = await db.coupons.insert_one(coupon_dict)
    return str(result.inserted_id)


async def get_coupon_by_id(db: AsyncIOMotorDatabase, coupon_id: str) -> Optional[CouponInDB]:
    """Get coupon by ID."""
    coupon_doc = await db.coupons.find_one({"_id": ObjectId(coupon_id)})
    if coupon_doc:
        coupon_doc["_id"] = str(coupon_doc["_id"])
        return CouponInDB(**coupon_doc)
    return None


async def get_coupon_by_barcode_and_client(db: AsyncIOMotorDatabase, barcode: str, client_id: str) -> Optional[CouponInDB]:
    """Get coupon by barcode and client ID."""
    coupon_doc = await db.coupons.find_one({"barcode": barcode, "client_id": client_id})
    if coupon_doc:
        coupon_doc["_id"] = str(coupon_doc["_id"])
        return CouponInDB(**coupon_doc)
    return None


async def get_coupons_by_client(db: AsyncIOMotorDatabase, client_id: str) -> List[CouponInDB]:
    """Get all coupons for a client."""
    coupons = []
    async for coupon_doc in db.coupons.find({"client_id": client_id}):
        coupon_doc["_id"] = str(coupon_doc["_id"])
        coupons.append(CouponInDB(**coupon_doc))
    return coupons


async def get_coupons_by_company(db: AsyncIOMotorDatabase, company_id: str) -> List[CouponInDB]:
    """Get all coupons for a company."""
    coupons = []
    async for coupon_doc in db.coupons.find({"company_id": company_id}):
        coupon_doc["_id"] = str(coupon_doc["_id"])
        coupons.append(CouponInDB(**coupon_doc))
    return coupons


async def update_coupon_count(db: AsyncIOMotorDatabase, coupon_id: str, new_count: int) -> bool:
    """Update coupon count."""
    result = await db.coupons.update_one(
        {"_id": ObjectId(coupon_id)},
        {"$set": {"count": new_count, "updated_at": datetime.now(timezone.utc)}}
    )
    return result.modified_count > 0


async def increment_coupon_count(db: AsyncIOMotorDatabase, coupon_id: str) -> bool:
    """Increment coupon count by 1."""
    result = await db.coupons.update_one(
        {"_id": ObjectId(coupon_id)},
        {"$inc": {"count": 1}, "$set": {"updated_at": datetime.now(timezone.utc)}}
    )
    return result.modified_count > 0


async def delete_coupon(db: AsyncIOMotorDatabase, coupon_id: str) -> bool:
    """Delete coupon by ID."""
    result = await db.coupons.delete_one({"_id": ObjectId(coupon_id)})
    return result.deleted_count > 0