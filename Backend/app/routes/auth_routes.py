from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import UserSignup, UserLogin, UserResponse
from app.services.auth_service import create_user, login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserSignup, db: Session = Depends(get_db)):

    new_user = create_user(db, user_data)

    return new_user


@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):

    token = login_user(db, login_data)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }