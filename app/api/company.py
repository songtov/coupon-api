from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.models.company import Company, CompanyCreate, CompanyUpdate
from app.models.user import User
from app.core.auth import get_current_admin
from app.db import get_db
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreate,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    company_data = company.dict()
    company_data["admin_id"] = str(current_user.id)
    company_data["created_at"] = datetime.utcnow()
    
    result = await db.companies.insert_one(company_data)
    created_company = await db.companies.find_one({"_id": result.inserted_id})
    
    return {**created_company, "id": str(created_company["_id"])}

@router.get("/", response_model=List[Company])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    companies = await db.companies.find(
        {"admin_id": str(current_user.id)}
    ).skip(skip).limit(limit).to_list(length=limit)
    
    return [{**company, "id": str(company["_id"])} for company in companies]

@router.get("/{company_id}", response_model=Company)
async def get_company(
    company_id: str,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    company = await db.companies.find_one({
        "_id": ObjectId(company_id),
        "admin_id": str(current_user.id)
    })
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return {**company, "id": str(company["_id"])}

@router.put("/{company_id}", response_model=Company)
async def update_company(
    company_id: str,
    company_update: CompanyUpdate,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    company = await db.companies.find_one({
        "_id": ObjectId(company_id),
        "admin_id": str(current_user.id)
    })
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    update_data = company_update.dict(exclude_unset=True)
    
    await db.companies.update_one(
        {"_id": ObjectId(company_id)},
        {"$set": update_data}
    )
    
    updated_company = await db.companies.find_one({"_id": ObjectId(company_id)})
    return {**updated_company, "id": str(updated_company["_id"])}

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: str,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    company = await db.companies.find_one({
        "_id": ObjectId(company_id),
        "admin_id": str(current_user.id)
    })
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    await db.companies.delete_one({"_id": ObjectId(company_id)})
    return None