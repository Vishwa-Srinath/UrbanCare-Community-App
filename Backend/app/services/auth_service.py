from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserSignup, UserLogin
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_access_token


from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.citizen import Citizen
from app.schemas.user_schema import UserSignup, UserLogin
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_access_token


def create_user(db: Session, user_data):

    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role
    )

    db.add(new_user)
    db.flush()

    # Create citizen profile automatically
    if user_data.role == "citizen":
        citizen = Citizen(user_id=new_user.user_id)
        db.add(citizen)

    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, login_data: UserLogin):

    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        return None

    if not verify_password(login_data.password, user.password_hash):
        return None

    return user


def login_user(db: Session, login_data: UserLogin):

    user = authenticate_user(db, login_data)

    if not user:
        return None

    token = create_access_token({
        "user_id": str(user.user_id),
        "role": user.role
    })

    return token