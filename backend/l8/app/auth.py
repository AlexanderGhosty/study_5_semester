from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError

SECRET = "dev-secret-change-me"
ALGO = "HS256"
ACCESS_MIN = 30

def create_access_token(sub: str, minutes: int = ACCESS_MIN) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=minutes)).timestamp())}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def verify_token(token: str) -> Optional[str]:
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return data.get("sub")
    except JWTError:
        return None
