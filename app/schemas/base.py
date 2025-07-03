from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.enum import SessionType

class PaginationInput(BaseModel):
    count: Optional[int] = 50
    page: Optional[int] = 0

class Pagination(BaseModel):
    count: int
    offset: Optional[int]
