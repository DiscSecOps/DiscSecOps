"""
Social feature schemas
Request and response models for Posts and Circles
"""
from datetime import datetime

from pydantic import BaseModel, Field
from backend.app.schemas.auth import UserResponse

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class PostCreate(PostBase):
    circle_id: int | None = Field(None, description="Optional Circle ID if posting to a circle")

class PostResponse(PostBase):
    id: int
    author_id: int
    circle_id: int | None
    created_at: datetime
    updated_at: datetime | None
    
    class Config:
        from_attributes = True

class CircleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)

class CircleCreate(CircleBase):
    pass

class CircleResponse(CircleBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CircleMemberResponse(BaseModel):
    circle_id: int
    user_id: int
    is_admin: bool
    is_moderator: bool
    joined_at: datetime

    class Config:
        from_attributes = True
