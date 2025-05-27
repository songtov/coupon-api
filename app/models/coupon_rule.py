from pydantic import BaseModel, Field


class CouponRuleBase(BaseModel):
    company_id: str
    required_coupons: int
    reward: str
    

class CouponRuleCreate(CouponRuleBase):
    pass
    

class CouponRuleInDB(CouponRuleBase):
    id: str = Field(..., alias="_id")
    

class CouponRule(CouponRuleBase):
    id: str