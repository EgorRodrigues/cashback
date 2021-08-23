from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class User(BaseModel):
    email: EmailStr

    @staticmethod
    def from_dict(obj) -> "User":
        return User(email=obj["email"])


class UserInDB(User):
    hashed_password: str

    @staticmethod
    def from_dict(obj) -> "UserInDB":
        return UserInDB(email=obj["email"], hashed_password=obj["password"])
