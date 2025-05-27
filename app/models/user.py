from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: str = Field(..., alias="_id")
    hashed_password: str
    

class User(UserBase):
    id: str