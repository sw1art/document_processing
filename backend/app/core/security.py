from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from pwdlib import PasswordHash

from backend.app.core.config import settings

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# JWT utils
def create_access_token(
    subject: str | int, expires_delta: Optional[timedelta] = None
) -> str:
    """
    subject: typically user id (UUID as str or int)
    returns: JWT token (str)
    """
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: Dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM_JWT)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Raises jwt.PyJWTError on invalid token.
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload
