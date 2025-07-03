from pydantic import BaseModel, EmailStr
from app.schemas.enum import Gender
from typing import List, Optional
from datetime import datetime, date

class SessionBase(BaseModel):
    organization_id: int
    type: str
    id: int
    session_name: str
    user_id: Optional[int]


class UserSimple(BaseModel):
    id : int
    name: str
    mobile_number: str
    gender: Gender
    profile_image: Optional[str] = None
    class Config:
        from_attributes = True