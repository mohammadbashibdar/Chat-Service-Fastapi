from pydantic import BaseModel

class TokenData(BaseModel):
    mobile_number: str | None = None
