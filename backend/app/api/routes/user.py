from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token
)

from app.services.auth_service import (
    create_user,
    login_user
)

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =====================================
# REGISTER
# =====================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = create_user(
        db=db,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    return user


# =====================================
# LOGIN
# =====================================

@router.post("/login")
def login(
    credentials: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    result = login_user(
        db=db,
        email=credentials.email,
        password=credentials.password
    )

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {result['access_token']}",
        httponly=True,
        samesite="lax",
        secure=False,  # Set to True in production if using HTTPS
        max_age=3600 * 24 * 7 # 7 days
    )

    # Serialize user model safely using UserResponse schema
    user_schema = UserResponse.model_validate(result["user"])

    return {
        "message": "Successfully logged in",
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user": user_schema
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False
    )
    return {"message": "Successfully logged out"}



# =====================================
# CURRENT USER PROFILE
# =====================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user