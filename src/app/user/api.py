from typing import List

from fastapi import APIRouter, Depends
from src.app.auth.models import User
from src.app.auth.auth import get_current_active_user
from src.app.auth import schemas as auth_schemas
from src.app.films.schemas import GetFilmReel

from src.app.user import service, models, schemas


user_router = APIRouter()


@user_router.get('/user/me', response_model=auth_schemas.User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@user_router.put('/user/update', response_model=auth_schemas.User)
async def read_users_me(user: schemas.UpdateUser, current_user: User = Depends(get_current_active_user)):
    return await service.user_s.update(user, id=current_user.id)


@user_router.post('/user/viewed', response_model=schemas.Messages)
async def user_viewed(pk: int, current_user: User = Depends(get_current_active_user)):
    return await service.user_s.viewed(pk, current_user)


@user_router.post('/user/cancel_viewed', response_model=schemas.Messages)
async def user_viewed(pk: int, current_user: User = Depends(get_current_active_user)):
    return await service.user_s.cancel_preview(pk, current_user)


@user_router.get('/user/all_viewed', response_model=List[GetFilmReel])
async def user_all_viewed(
        film_reel_type: models.ModelNameFilmReel,
        current_user: User = Depends(get_current_active_user)
):
    return await service.user_s.all_viewed(film_reel_type, current_user)
