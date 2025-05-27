from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.coupon_rule import CouponRuleCreate, CouponRuleInDB, CouponRule


async def create_coupon_rule(db: AsyncIOMotorDatabase, coupon_rule: CouponRuleCreate) -> str:
    """Create a new coupon rule in the database."""
    coupon_rule_dict = coupon_rule.model_dump()
    
    result = await db.coupon_rules.insert_one(coupon_rule_dict)
    return str(result.inserted_id)


async def get_coupon_rule_by_id(db: AsyncIOMotorDatabase, rule_id: str) -> Optional[CouponRuleInDB]:
    """Get coupon rule by ID."""
    rule_doc = await db.coupon_rules.find_one({"_id": ObjectId(rule_id)})
    if rule_doc:
        rule_doc["_id"] = str(rule_doc["_id"])
        return CouponRuleInDB(**rule_doc)
    return None


async def get_coupon_rules_by_company(db: AsyncIOMotorDatabase, company_id: str) -> List[CouponRuleInDB]:
    """Get all coupon rules for a company."""
    rules = []
    async for rule_doc in db.coupon_rules.find({"company_id": company_id}):
        rule_doc["_id"] = str(rule_doc["_id"])
        rules.append(CouponRuleInDB(**rule_doc))
    return rules


async def update_coupon_rule(db: AsyncIOMotorDatabase, rule_id: str, update_data: dict) -> bool:
    """Update coupon rule data."""
    result = await db.coupon_rules.update_one(
        {"_id": ObjectId(rule_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0


async def delete_coupon_rule(db: AsyncIOMotorDatabase, rule_id: str) -> bool:
    """Delete coupon rule by ID."""
    result = await db.coupon_rules.delete_one({"_id": ObjectId(rule_id)})
    return result.deleted_count > 0