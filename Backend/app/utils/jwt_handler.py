from jose import jwt, JWTError
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("JWT_SECRET")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_HOURS=24

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        return payload
    except JWTError:
        return None




