from typing import Optional, List
from sqlalchemy.orm import Session
from app.domains.common.base_repository import BaseRepository
from app.domains.users.models.user import User

class UserRepository(BaseRepository[User]):
    """Repository for the User aggregate.
    Provides basic CRUD plus email lookup.
    """

    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def list(self) -> List[User]:
        return self.session.query(User).all()

    def update_user(self, user: User, **kwargs) -> User:
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        self.session.commit()
        self.session.refresh(user)
        return user
