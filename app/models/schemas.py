from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Any


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16)
    role: str = Field("user", description="Role of the user, e.g., 'user' or 'admin'")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one numeric character')
        if not any(char in "@$!%*?&" for char in value):
            raise ValueError('Password must contain at least one special character (@$!%*?&)')
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    owner_email: str
