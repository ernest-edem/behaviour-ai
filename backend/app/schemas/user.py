from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


# =====================================
# USER CREATE
# =====================================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# =====================================
# USER LOGIN
# =====================================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =====================================
# USER UPDATE PROFILE
# =====================================

class UserUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None

    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None

    blood_group: Optional[str] = None


# =====================================
# USER RESPONSE (SAFE - NO PASSWORD)
# =====================================

class UserResponse(BaseModel):
    id: int

    name: str
    email: EmailStr

    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None

    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None

    blood_group: Optional[str] = None

    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================
# AUTH TOKEN
# =====================================

class Token(BaseModel):
    access_token: str
    token_type: str


# =====================================
# TOKEN PAYLOAD
# =====================================

class TokenData(BaseModel):
    user_id: Optional[int] = None