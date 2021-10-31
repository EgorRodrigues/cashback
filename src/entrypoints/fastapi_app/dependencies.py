from fastapi import Depends

from src.auth.repository import DatabaseRepository
from src.auth.schemas import User
from src.auth.services import AuthService
from src.db import database
from src.orm import resellers

repository = DatabaseRepository(database, resellers)


async def get_current_user(
    current_user: User = Depends(AuthService(repository).get_current_user),
):
    return current_user
