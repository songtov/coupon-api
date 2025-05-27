from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    

class CompanyCreate(CompanyBase):
    admin_id: str
    

class CompanyInDB(CompanyBase):
    id: str = Field(..., alias="_id")
    admin_id: str
    created_at: datetime
    

class Company(CompanyBase):
    id: str
    admin_id: str