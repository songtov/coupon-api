from pydantic import BaseModel, Field
from typing import Optional


class CouponRuleBase(BaseModel):
    company_id: str
    required_coupons: int
    reward: str
    

class CouponRuleCreate(CouponRuleBase):
    pass


class CouponRuleUpdate(BaseModel):
    company_id: Optional[str] = None
    required_coupons: Optional[int] = None
    reward: Optional[str] = None
    

class CouponRuleInDB(CouponRuleBase):
    id: str = Field(..., alias="_id")
    

class CouponRule(CouponRuleBase):
    id: str