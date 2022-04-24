from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.auth import models


User = pydantic_model_creator(models.User, name="get_user", exclude=('hashed_password',))


class TokenPayload(BaseModel):
    user_id: int = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserName(BaseModel):
    username: str


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
