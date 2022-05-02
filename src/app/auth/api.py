from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.app.auth import schemas
from src.app.auth import service

user_router = APIRouter()


@user_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await service.user_s.auth(form_data.username, form_data.password)


@user_router.post("/user/create", response_model=schemas.User)
async def create_user(user: schemas.CreateUser):
    return await service.user_s.create(schema=user)
