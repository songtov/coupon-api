from typing import Optional, List
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.company import CompanyCreate, CompanyInDB, Company


async def create_company(db: AsyncIOMotorDatabase, company: CompanyCreate) -> str:
    """Create a new company in the database."""
    company_dict = company.model_dump()
    company_dict["created_at"] = datetime.now(timezone.utc)
    
    result = await db.companies.insert_one(company_dict)
    return str(result.inserted_id)


async def get_company_by_id(db: AsyncIOMotorDatabase, company_id: str) -> Optional[CompanyInDB]:
    """Get company by ID."""
    company_doc = await db.companies.find_one({"_id": ObjectId(company_id)})
    if company_doc:
        company_doc["_id"] = str(company_doc["_id"])
        return CompanyInDB(**company_doc)
    return None


async def get_companies_by_admin(db: AsyncIOMotorDatabase, admin_id: str) -> List[CompanyInDB]:
    """Get all companies managed by an admin."""
    companies = []
    async for company_doc in db.companies.find({"admin_id": admin_id}):
        company_doc["_id"] = str(company_doc["_id"])
        companies.append(CompanyInDB(**company_doc))
    return companies


async def get_all_companies(db: AsyncIOMotorDatabase) -> List[CompanyInDB]:
    """Get all companies."""
    companies = []
    async for company_doc in db.companies.find():
        company_doc["_id"] = str(company_doc["_id"])
        companies.append(CompanyInDB(**company_doc))
    return companies


async def update_company(db: AsyncIOMotorDatabase, company_id: str, update_data: dict) -> bool:
    """Update company data."""
    result = await db.companies.update_one(
        {"_id": ObjectId(company_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0


async def delete_company(db: AsyncIOMotorDatabase, company_id: str) -> bool:
    """Delete company by ID."""
    result = await db.companies.delete_one({"_id": ObjectId(company_id)})
    return result.deleted_count > 0