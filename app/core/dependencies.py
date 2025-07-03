from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.auth import oauth2_scheme
from app.core.config import settings
from app.core.database import get_db
from app.schemas.token import TokenData
from app.models.user import User

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Dependency to get the current authenticated user.
    """
    from app.crud.user import get_user_by_mobile
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        mobile_number: str = payload.get("sub")
        if mobile_number is None:
            raise credentials_exception
        token_data = TokenData(mobile_number=mobile_number)
    except JWTError:
        raise credentials_exception

    user = await get_user_by_mobile(db, mobile_number=token_data.mobile_number)
    if user is None:
        raise credentials_exception
    return user
