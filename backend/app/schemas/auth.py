from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    role: str
    is_active: bool


class CurrentUser(BaseModel):
    id: int
    full_name: str
    username: str
    role: str
    is_active: bool


class UserCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=150)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(default="operator", max_length=50)
