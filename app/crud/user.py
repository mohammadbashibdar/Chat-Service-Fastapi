from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.enum import Gender
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload, selectinload
from datetime import datetime
from sqlalchemy import or_


async def get_user_by_mobile(db: AsyncSession, mobile_number: str) -> User | None:
    """Fetch a user by their mobile number, including related data."""
    query = (
        select(User)
        .options(
            selectinload(User.building),
            selectinload(User.groups),
            selectinload(User.roles),
        )
        .filter(User.mobile_number == mobile_number)
    )
    result = await db.execute(query)
    return result.scalars().first()
