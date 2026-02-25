from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.endpoints.auth import get_current_user_from_session
from app.core.db import get_db
from app.db.models import Circle, CircleMember, User
from app.schemas.social import (
    CircleCreate,
    CircleMemberResponse,
    CircleResponse,
    CircleRole,
)

router = APIRouter(prefix="/circles", tags=["Circles"])


@router.get("/my", response_model=list[CircleResponse])
async def get_my_circles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> list[CircleResponse]:
    """
    Get circles where current user is a member
    Used for dashboard display with roles and badges
    """
    # Get all circles where user is a member, with member info
    circles_result = await db.execute(
        select(Circle)
        .join(CircleMember, Circle.id == CircleMember.circle_id)
        .where(CircleMember.user_id == current_user.id)
        .options(selectinload(Circle.members))
        .order_by(Circle.created_at.desc())
    )
    circles = circles_result.scalars().all()

    # Build response with member info and badges
    result = []
    for circle in circles:
        # Count total members
        member_count = len(circle.members)

        # Get owner info
        owner = await db.get(User, circle.owner_id)

        result.append(
            CircleResponse(
                id=circle.id,
                name=circle.name,
                description=circle.description,
                owner_id=circle.owner_id,
                owner_name=owner.username if owner else None,
                members=[
                    CircleMemberResponse(
                        circle_id=m.circle_id,
                        user_id=m.user_id,
                        username=(await db.get(User, m.user_id)).username,
                        role=m.role,
                        badge={
                            CircleRole.OWNER: "👑",
                            CircleRole.MODERATOR: "🛡️",
                            CircleRole.MEMBER: "👤"
                        }.get(m.role, "👤"),
                        joined_at=m.joined_at
                    )
                    for m in circle.members
                ],
                member_count=member_count,
                created_at=circle.created_at
            )
        )

    return result


@router.post("/", response_model=CircleResponse, status_code=status.HTTP_201_CREATED)
async def create_circle(
    circle_data: CircleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> CircleResponse:
    """
    Create a new circle
    User becomes owner and first member
    """
    # Check if circle name is already taken
    existing = await db.execute(
        select(Circle).where(Circle.name == circle_data.name)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A circle with this name already exists"
        )

    # Create circle
    new_circle = Circle(
        name=circle_data.name,
        description=circle_data.description,
        owner_id=current_user.id
    )
    db.add(new_circle)
    await db.flush()  # Get circle ID without commit

    # Add owner as member with role "owner"
    owner_member = CircleMember(
        circle_id=new_circle.id,
        user_id=current_user.id,
        role=CircleRole.OWNER
    )
    db.add(owner_member)

    await db.commit()
    await db.refresh(new_circle)

    # Get owner username for response
    owner = await db.get(User, current_user.id)

    return CircleResponse(
        id=new_circle.id,
        name=new_circle.name,
        description=new_circle.description,
        owner_id=new_circle.owner_id,
        owner_name=owner.username,
        members=[
            CircleMemberResponse(
                circle_id=new_circle.id,
                user_id=current_user.id,
                username=owner.username,
                role=CircleRole.OWNER,
                badge="👑",
                joined_at=owner_member.joined_at
            )
        ],
        member_count=1,
        created_at=new_circle.created_at
    )


@router.get("/{circle_id}", response_model=CircleResponse)
async def get_circle(
    circle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> CircleResponse:
    """
    Get circle details by ID
    User must be a member to view
    """
    # Get circle with members
    circle_result = await db.execute(
        select(Circle)
        .where(Circle.id == circle_id)
        .options(selectinload(Circle.members))
    )
    circle = circle_result.scalar_one_or_none()

    if not circle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circle not found"
        )

    # Check if user is a member
    user_member = next(
        (m for m in circle.members if m.user_id == current_user.id),
        None
    )
    if not user_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this circle"
        )

    # Get usernames for all members
    member_responses = []
    for member in circle.members:
        user_result = await db.get(User, member.user_id)
        member_responses.append(
            CircleMemberResponse(
                circle_id=member.circle_id,
                user_id=member.user_id,
                username=user_result.username,
                role=member.role,
                badge={
                    CircleRole.OWNER: "👑",
                    CircleRole.MODERATOR: "🛡️",
                    CircleRole.MEMBER: "👤"
                }.get(member.role, "👤"),
                joined_at=member.joined_at
            )
        )

    # Get owner
    owner = await db.get(User, circle.owner_id)

    return CircleResponse(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        owner_id=circle.owner_id,
        owner_name=owner.username,
        members=member_responses,
        member_count=len(circle.members),
        created_at=circle.created_at
    )


@router.put("/{circle_id}")
async def update_circle(
    circle_id: int,
    circle_data: CircleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> CircleResponse:
    """
    Update circle details (owner only)
    """
    circle = await db.get(Circle, circle_id)

    if not circle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circle not found"
        )

    # Check if user is owner
    if circle.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the circle owner can update it"
        )

    # Update fields
    circle.name = circle_data.name
    circle.description = circle_data.description

    await db.commit()
    await db.refresh(circle)

    # Return updated circle
    return await get_circle(circle_id, db, current_user)


@router.delete("/{circle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circle(
    circle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session)
) -> None:
    """
    Delete a circle (owner only)
    """
    circle = await db.get(Circle, circle_id)

    if not circle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Circle not found"
        )

    # Check if user is owner
    if circle.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the circle owner can delete it"
        )

    # Delete circle (cascade will delete members and posts)
    await db.delete(circle)
    await db.commit()
