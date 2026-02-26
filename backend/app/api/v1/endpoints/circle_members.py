# app/api/v1/endpoints/circle_members.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.auth import get_current_user_from_session
from app.core.db import get_db
from app.db.models import Circle, CircleMember, User
from app.schemas.social import (
    AddMemberRequest,
    CircleMemberResponse,
    CircleRole,
    MemberActionResponse,
    UpdateRoleRequest,
)

router = APIRouter(prefix="/circles", tags=["Circle Members"])


# ======================================================
# 1. ADD MEMBER TO CIRCLE
# ======================================================
@router.post("/{circle_id}/members", status_code=201, response_model=MemberActionResponse)
async def add_member(
    circle_id: int,
    request: AddMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> MemberActionResponse:
    """
    Add a user to circle (owner/moderator only)
    - New member gets 'member' role
    - Returns member data with badge
    """
    # 1. Check if circle exists
    circle = await db.get(Circle, circle_id)
    if not circle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circle not found"
        )

    # 2. Check if current user has permission (owner or moderator)
    permission = await db.execute(
        select(CircleMember)
        .where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == current_user.id,
            CircleMember.role.in_(["owner", "moderator"])
        )
    )
    if not permission.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only circle owners and moderators can add members"
        )

    # 3. Check if user to add exists
    user_to_add = await db.get(User, request.user_id)
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 4. Check if already a member
    existing = await db.execute(
        select(CircleMember)
        .where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == request.user_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this circle"
        )

    # 5. Add new member
    new_member = CircleMember(
        circle_id=circle_id,
        user_id=request.user_id,
        role=CircleRole.MEMBER,
        joined_at=datetime.now()
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)

    # 6. Return response with badge
    member_response = CircleMemberResponse(
        circle_id=new_member.circle_id,
        user_id=new_member.user_id,
        username=user_to_add.username,
        role=new_member.role,
        joined_at=new_member.joined_at
    )

    return MemberActionResponse(
        success=True,
        message="Member added successfully",
        member=member_response
    )


# ======================================================
# 2. REMOVE MEMBER FROM CIRCLE
# ======================================================
@router.delete("/{circle_id}/members/{user_id}", response_model=MemberActionResponse)
async def remove_member(
    circle_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> MemberActionResponse:
    """
    Remove member from circle
    - Owner can remove anyone (including moderators)
    - Moderator can remove members (not other moderators or owner)
    """
    # 1. Check if circle exists
    circle = await db.get(Circle, circle_id)
    if not circle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circle not found"
        )

    # 2. Get member to remove
    member_result = await db.execute(
        select(CircleMember)
        .where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == user_id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found in this circle"
        )

    # 3. Cannot remove the owner
    if member.role == CircleRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot remove the circle owner"
        )

    # 4. Get current user's role
    current_member = await db.execute(
        select(CircleMember)
        .where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == current_user.id
        )
    )
    current = current_member.scalar_one_or_none()

    if not current:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this circle"
        )

    # 5. Check permissions
    if current.role == CircleRole.OWNER:
        # Owner can remove anyone (except owner, already checked)
        pass
    elif current.role == CircleRole.MODERATOR:
        # Moderator can only remove members (not other moderators)
        if member.role == CircleRole.MODERATOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Moderators cannot remove other moderators"
            )
    else:
        # Members cannot remove anyone
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners and moderators can remove members"
        )

    # 6. Remove member
    username = (await db.get(User, user_id)).username
    await db.delete(member)
    await db.commit()

    return MemberActionResponse(
        success=True,
        message=f"Member {username} removed successfully",
        member=None
    )


# ======================================================
# 3. UPDATE MEMBER ROLE
# ======================================================
@router.put("/{circle_id}/members/{user_id}/role", response_model=MemberActionResponse)
async def update_member_role(
    circle_id: int,
    user_id: int,
    request: UpdateRoleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> MemberActionResponse:
    """
    Change member's role (owner only)
    - Owner can promote to moderator
    - Owner can demote moderator to member
    - Cannot change owner's role
    """
    # 1. Check if current user is OWNER
    owner_check = await db.execute(
        select(CircleMember)
        .where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == current_user.id,
            CircleMember.role == CircleRole.OWNER
        )
    )
    if not owner_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the circle owner can change roles"
        )

    # 2. Get member to update
    member_result = await db.execute(
        select(CircleMember)
        .where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == user_id
        )
    )
    member = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found in this circle"
        )

    # 3. Cannot change owner's role
    if member.role == CircleRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot change the circle owner's role"
        )

    # 4. Update role
    old_role = member.role
    member.role = request.role
    await db.commit()
    await db.refresh(member)

    # 5. Get username for response
    user = await db.get(User, user_id)

    member_response = CircleMemberResponse(
        circle_id=member.circle_id,
        user_id=member.user_id,
        username=user.username,
        role=member.role,
        joined_at=member.joined_at
    )

    return MemberActionResponse(
        success=True,
        message=f"Role changed from {old_role} to {request.role}",
        member=member_response
    )
