from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=60)
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(default="reader")  # admin|writer|reader

class UserRead(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool