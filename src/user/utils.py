from datetime import datetime, timedelta, timezone
from typing import Any
import jwt


def create_access_token(
    *,
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
    secret_key: str,
    algorithm: str
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(  # type: ignore
        to_encode, key=secret_key, algorithm=algorithm
    )
    return encoded_jwt
