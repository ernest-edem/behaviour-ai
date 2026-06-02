from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.core.security import decode_access_token


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token_str = request.cookies.get("access_token")
    
    if not token_str:
        # Fallback to Authorization header if necessary for other API clients
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token_str = auth_header
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

    # Strip "Bearer " prefix if present
    if token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
    else:
        token = token_str

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_id = payload.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user