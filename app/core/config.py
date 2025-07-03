from fastapi import HTTPException, status, Depends
from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, ClassVar
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chat FastAPI App"
    DATABASE_URL: str = "postgres://Bashibdar:postgres@localhost:5445/db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    oauth2_scheme: ClassVar[OAuth2PasswordBearer] = OAuth2PasswordBearer(tokenUrl="token")
    LoginFormDep: ClassVar[Annotated[OAuth2PasswordRequestForm, Depends()]] = Annotated[OAuth2PasswordRequestForm, Depends()]
    TokenDep: ClassVar[Annotated[str, Depends(oauth2_scheme)]] = Annotated[str, Depends(oauth2_scheme)]


    class Config:
        env_file = ".env"

settings = Settings()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)