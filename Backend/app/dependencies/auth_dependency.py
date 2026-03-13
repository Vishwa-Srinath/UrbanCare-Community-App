from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.jwt_handler import verify_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload


def require_role(required_role: str):

    def role_checker(user = Depends(get_current_user)):

        if user["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return user

    return role_checker