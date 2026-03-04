from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(*, subject: str, secret_key: str, algorithm: str, expires_minutes: int, extra: dict[str, Any] | None = None) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    payload: dict[str, Any] = {"sub": subject, "iat": int(now.timestamp()), "exp": int(expire.timestamp())}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, secret_key, algorithm=algorithm)

def decode_token(token: str, *, secret_key: str, algorithm: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError as e:
        raise ValueError("Invalid token") from e