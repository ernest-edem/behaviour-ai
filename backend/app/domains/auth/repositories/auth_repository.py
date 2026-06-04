from sqlalchemy.orm import Session
from app.models.user import User

class AuthRepository:
    """Placeholder repository for auth‑specific data (e.g., login audit)."""

    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    # Future methods: store_login_attempt, revoke_sessions, etc.
