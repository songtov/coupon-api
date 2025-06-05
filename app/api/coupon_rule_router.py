from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.coupon_rule import CouponRule, CouponRuleCreate, CouponRuleUpdate, CouponRuleInDB
from app.models.user import User
from app.core.auth import get_current_admin
from app.db import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=CouponRule, status_code=status.HTTP_201_CREATED)
async def create_coupon_rule(
    rule: CouponRuleCreate,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    # Verify company exists and belongs to admin
    company = await db.companies.find_one({
        "_id": ObjectId(rule.company_id),
        "admin_id": str(current_user.id)
    })
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found or you don't have permission"
        )
    # Validate rule parameters
    if rule.required_coupons <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required coupons must be greater than 0"
        )
    rule_data = rule.model_dump()
    result = await db.coupon_rules.insert_one(rule_data)
    created_rule = await db.coupon_rules.find_one({"_id": result.inserted_id})
    return {**created_rule, "id": str(created_rule["_id"])}

@router.get("/company/{company_id}", response_model=List[CouponRule])
async def list_company_rules(
    company_id: str,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    # Verify company exists and belongs to admin
    company = await db.companies.find_one({
        "_id": ObjectId(company_id),
        "admin_id": str(current_user.id)
    })
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found or you don't have permission"
        )
    rules = await db.coupon_rules.find({"company_id": company_id}).to_list(length=100)
    return [{**rule, "id": str(rule["_id"])} for rule in rules]

@router.get("/{rule_id}", response_model=CouponRule)
async def get_coupon_rule(
    rule_id: str,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    rule = await db.coupon_rules.find_one({"_id": ObjectId(rule_id)})
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    # Verify company belongs to admin
    company = await db.companies.find_one({
        "_id": ObjectId(rule["company_id"]),
        "admin_id": str(current_user.id)
    })
    if not company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this rule"
        )
    return {**rule, "id": str(rule["_id"])}

@router.put("/{rule_id}", response_model=CouponRule)
async def update_coupon_rule(
    rule_id: str,
    rule_update: CouponRuleUpdate,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    rule = await db.coupon_rules.find_one({"_id": ObjectId(rule_id)})
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    # Verify company belongs to admin
    company = await db.companies.find_one({
        "_id": ObjectId(rule["company_id"]),
        "admin_id": str(current_user.id)
    })
    if not company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this rule"
        )
    update_data = rule_update.model_dump(exclude_unset=True)
    if "required_coupons" in update_data and update_data["required_coupons"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required coupons must be greater than 0"
        )
    await db.coupon_rules.update_one(
        {"_id": ObjectId(rule_id)},
        {"$set": update_data}
    )
    updated_rule = await db.coupon_rules.find_one({"_id": ObjectId(rule_id)})
    return {**updated_rule, "id": str(updated_rule["_id"])}

@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coupon_rule(
    rule_id: str,
    current_user: User = Depends(get_current_admin),
    db = Depends(get_db)
):
    rule = await db.coupon_rules.find_one({"_id": ObjectId(rule_id)})
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    # Verify company belongs to admin
    company = await db.companies.find_one({
        "_id": ObjectId(rule["company_id"]),
        "admin_id": str(current_user.id)
    })
    if not company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this rule"
        )
    await db.coupon_rules.delete_one({"_id": ObjectId(rule_id)})
    return None 