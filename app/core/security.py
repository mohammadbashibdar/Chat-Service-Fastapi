from typing import Annotated, Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.security import TokenData
from app.core.auth import oauth2_scheme  # Updated import


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        current_session = payload.get("current_session")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION

    result = await session.execute(select(User).where(User.mobile_number == token_data.username))
    user = result.scalar_one_or_none()
    if user is None:
        raise CREDENTIALS_EXCEPTION

    # Attach current_session to the user object for later use
    user.current_session = current_session
    return user


async def get_current_session(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        current_session = payload.get("current_session")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION

    result = await session.execute(select(User).where(User.mobile_number == token_data.username))
    user = result.scalar_one_or_none()
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return current_session

