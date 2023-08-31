from pydantic import BaseModel, EmailStr
from .config import TunedModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: Optional[str]
    subtitle: Optional[str]
    user_id: int
    image: str

class PostRead(TunedModel):
    id: int
    title: str | None
    subtitle: str | None
    image: str
    likes: int
    user_id: int
    created_at: datetime

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

class PostSend(PostRead):
    user: UserRead 