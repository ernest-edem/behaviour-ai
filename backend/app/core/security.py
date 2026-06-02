from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings

# ==========================================
# CONFIG
# ==========================================

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# 30 days refresh token
REFRESH_TOKEN_EXPIRE_DAYS = 30

# ==========================================
# PASSWORD HASHING
# ==========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================
# ACCESS TOKEN
# ==========================================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + (
            expires_delta
            or timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================
# REFRESH TOKEN
# ==========================================

def create_refresh_token(
    data: dict
):
    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================
# TOKEN DECODE
# ==========================================

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None


# Backward compatibility
def decode_token(token: str):
    return decode_access_token(token)


# ==========================================
# USER ID HELPER
# ==========================================

def get_user_id_from_token(
    token: str
):
    payload = decode_access_token(token)

    if not payload:
        return None

    return payload.get("user_id")