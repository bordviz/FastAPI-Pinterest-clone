from datetime import datetime
from pydantic import BaseModel, EmailStr
from .config import TunedModel
from typing import List
from .post import PostRead

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str 
    email: EmailStr
    hashed_password: str

class UserRead(TunedModel):
    id: int
    first_name: str
    last_name: str
    username: str 
    email: EmailStr
    subscriptions: int
    subscribers: int
    avatar_image: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserProfile(UserRead):
    posts: List[PostRead]