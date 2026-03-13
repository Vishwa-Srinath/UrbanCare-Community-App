from pydantic import BaseModel, EmailStr, constr
from uuid import UUID


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8, max_length=64)
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: UUID
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True