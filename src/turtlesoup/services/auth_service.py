import os
from dotenv import load_dotenv
from datetime import date, datetime, time, timezone
from typing import Any

import jwt


load_dotenv()


class AuthService:
    def __init__(
        self
    ) -> None:
        self._secret_key = os.getenv("JWT_SECRET_KEY", "test")
        

    def create_jwt(
        self,
        payload: dict[str, Any],
        expires_at: datetime | date,
    ) -> str:
        if isinstance(expires_at, datetime):
            expiration = expires_at
        else:
            expiration = datetime.combine(expires_at, time.min)

        if expiration.tzinfo is None:
            expiration = expiration.replace(tzinfo=timezone.utc)

        claims = {**payload, "exp": expiration}
        return jwt.encode(claims, self._secret_key, algorithm="HS256")
