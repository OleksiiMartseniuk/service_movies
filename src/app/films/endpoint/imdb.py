from typing import List

from fastapi_pagination import Page, paginate

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.app.films import schemas, service

imdb_router = APIRouter()


@imdb_router.get('/group/{pk}',  response_model=schemas.GetGroup, responses={404: {"model": HTTPNotFoundError}})
async def get_group(pk: int):
    """ Вывод групи """
    return await service.group_s.get(id=pk)


@imdb_router.get('/groups',  response_model=List[schemas.GetGroup], responses={404: {"model": HTTPNotFoundError}})
async def get_group():
    """ Вывод всех груп """
    return await service.group_s.all()


@imdb_router.get('/movie/{pk}',  response_model=schemas.GetMovie, responses={404: {"model": HTTPNotFoundError}})
async def get_group(pk: int):
    """ Вывод фильма """
    return await service.movie_s.get(id=pk)


@imdb_router.get('/movies/{group_id}',  response_model=Page[schemas.GetMovie], responses={404: {"model": HTTPNotFoundError}})
async def get_group(group_id: int):
    """ Вывод всех фильмов  """
    movies = await service.movie_s.all(group_id=group_id)
    return paginate(movies)
