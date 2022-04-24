import jwt
from typing import Optional
from datetime import datetime, timedelta
from src.config import settings


def create_token(user_id: int) -> dict:
    """ Создания токена """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': create_access_token(
            data={'sub': user_id}, expires_delta=access_token_expires
        ),
        'token_type': 'bearer'
    }


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """ Создания access токена """
    to_code = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_code.update({'exp': expire})
    encoded_jwt = jwt.encode(to_code, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
