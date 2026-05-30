from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


# =====================================
# GET USER BY EMAIL
# =====================================

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# =====================================
# CREATE NEW USER (REGISTER)
# =====================================

def create_user(db: Session, name: str, email: str, password: str):
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return None  # user already exists

    # Hash password
    hashed_password = hash_password(password)

    # Create user object
    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        is_active=True,
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =====================================
# AUTHENTICATE USER (LOGIN)
# =====================================

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# =====================================
# LOGIN + TOKEN GENERATION
# =====================================

def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    if not user:
        return None

    token = create_access_token(
        data={"user_id": user.id, "email": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }