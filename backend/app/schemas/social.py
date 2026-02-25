"""
Social feature schemas
Request and response models for Posts and Circles
"""
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    circle_id: int | None = Field(None, description="Optional Circle ID if posting to a circle")


class PostResponse(PostBase):
    id: int
    author_id: int
    author_name: str | None = Field(None, description="Username of author") # Optional for frontend
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


class CircleRole(StrEnum):
    OWNER = "owner"
    MODERATOR = "moderator"
    MEMBER = "member"


class CircleMemberResponse(BaseModel):
    circle_id: int
    user_id: int
    username: str | None = Field(None, description="Username of member")  # Pentru afișare
    role: CircleRole
    badge: str | None = Field(None, description="👑, 🛡️, 👤 - calculated from role")
    joined_at: datetime

    class Config:
        from_attributes = True

    def model_post_init(self, __context) -> None:
        """Calculate badge after initialization"""
        badge_map = {
            CircleRole.OWNER: "👑",
            CircleRole.MODERATOR: "🛡️",
            CircleRole.MEMBER: "👤"
        }
        self.badge = badge_map.get(self.role, "👤")


class CircleResponse(CircleBase):
    id: int
    owner_id: int
    owner_name: str | None = Field(None, description="Username of owner")
    members: list[CircleMemberResponse] | None = Field(None, description="Circle members")
    member_count: int | None = Field(None, description="Total number of members")
    created_at: datetime

    class Config:
        from_attributes = True


# Pentru request-uri de update role (admin/mod only)
class CircleMemberUpdate(BaseModel):
    role: CircleRole
