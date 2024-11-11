from pydantic import BaseModel, ConfigDict
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None
    role: str = "user"
    disabled: bool | None = None


class UserInDB(User):
    id: int
    hashed_password: str


class UserResponce(BaseModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    role: str = "user"
    disabled: bool | None = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = "user"
    disabled: Optional[bool] = None
