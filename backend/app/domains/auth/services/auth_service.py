from typing import Any
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import verify_password, create_access_token
from app.domains.auth.repositories.user_repository import UserRepository
from app.domains.auth.schemas import UserCreate, UserLogin, UserResponse

class AuthService:
    """Business logic for authentication and user session management.

    All operations are performed via the `UserRepository` which isolates
    persistence concerns. No direct SQLAlchemy calls are made here.
    """

    def __init__(self, db: Session = Depends(get_db)):
        self.repo = UserRepository(db)

    def register_user(self, payload: UserCreate) -> UserResponse:
        # Validate uniqueness of email
        if self.repo.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        # Hash password and create user
        user = self.repo.create_user(
            name=payload.name,
            email=payload.email,
            password_hash=payload.password,  # repository will hash
        )
        return UserResponse.from_orm(user)

    def login_user(self, credentials: UserLogin) -> dict:
        user = self.repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        access_token = create_access_token({"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    def logout_user(self) -> dict:
        # No persistence needed – logout is handled by clearing the cookie on the client
        return {"message": "Successfully logged out"}
