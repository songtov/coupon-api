from pydantic import BaseModel, Field
from datetime import datetime


class CouponBase(BaseModel):
    company_id: str
    barcode: str
    

class CouponCreate(CouponBase):
    pass
    

class CouponInDB(CouponBase):
    id: str = Field(..., alias="_id")
    client_id: str
    count: int = 0
    created_at: datetime
    updated_at: datetime
    

class Coupon(CouponBase):
    id: str
    client_id: str
    count: int