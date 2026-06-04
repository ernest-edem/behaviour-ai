from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.domains.users.repositories.user_repository import UserRepository
from app.domains.users.schemas import UserResponse, UserUpdate

class UserService:
    """Business logic for user management.

    All persistence is delegated to :class:`UserRepository`. The service
    validates input, handles domain‑specific rules and raises appropriate
    HTTP errors that the API layer can translate directly.
    """

    def __init__(self, db: Session = Depends(get_db)):
        self.repo = UserRepository(db)

    def get_user(self, user_id: int) -> UserResponse:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.from_orm(user)

    def list_users(self) -> List[UserResponse]:
        users = self.repo.list()
        return [UserResponse.from_orm(u) for u in users]

    def update_user(self, user_id: int, payload: UserUpdate) -> UserResponse:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        updated_user = self.repo.update_user(user, **payload.dict(exclude_unset=True))
        return UserResponse.from_orm(updated_user)

    def delete_user(self, user_id: int) -> None:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        self.repo.delete(user)
        # No return needed; API will send 204 No Content
