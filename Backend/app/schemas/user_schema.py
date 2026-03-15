from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    citizen = "citizen"
    authority = "authority"
    admin = "admin"

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: UUID
    name: str
    email: str
    phone_number: str
    role: str

    class Config:
        from_attributes = True



