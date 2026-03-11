from pydantic import BaseModel, EmilStr

class UserSignup(BaseModel):
    name :str
    email :EmilStr
    password :str
    role : str

class UserLogin(BaseModel):
    email : EmilStr
    password : str

class UserResponse(BaseModel):
    user_id:str
    name : str
    email : str
    role : str

class Config:
    from_attribute=True