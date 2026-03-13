from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.utils.jwt_handler import verify_token


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request.state.user = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):

            token = auth_header.split(" ")[1]

            payload = verify_token(token)

            if payload:
                request.state.user = payload

        response = await call_next(request)

        return response
    