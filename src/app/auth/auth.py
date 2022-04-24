import jwt
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.config import settings
from src.app.auth import schemas, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password, hashed_password) -> bool:
    """ Сравнения хеш"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """ Получения шех-пароля """
    return pwd_context.hash(password)


async def get_user(username: str) -> models.User:
    """ Получения пользователя по username """
    user_name = schemas.UserName(username=username)
    return await models.User.get_or_none(**user_name.dict())


async def authenticate_user(username: str, password: str) -> Union[models.User, bool]:
    """ Аутентификация пользователя """
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    """ Проверить авторизацию пользователя """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        token_data = schemas.TokenPayload(user_id=user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await models.User.get_or_none(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    """ Проверить активный пользователя """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
