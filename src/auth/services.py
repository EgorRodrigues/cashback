from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from prettyconf import config
from starlette import status

from src.auth.exceptions import UserDoesNotExist
from src.auth.repository import Repository
from src.auth.schemas import TokenData, User, UserInDB

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
TOKEN_URL = config("TOKEN_URL")


class AuthService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, repository: Repository):
        self.repository = repository

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    async def authenticate_user(
        self, email: str, password: str
    ) -> Union[UserInDB, bool]:
        result = await self.repository.get_by_email(email)
        if not self.verify_password(password, result["password"]):
            return False
        return UserInDB.from_dict(result)

    @staticmethod
    async def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
            user = await self.repository.get_by_email(str(token_data.email))
        except JWTError:
            raise credentials_exception
        except UserDoesNotExist:
            raise credentials_exception
        return User.from_dict(user)
