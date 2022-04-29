from typing import List

from fastapi_pagination import Page, paginate, Params
from fastapi import APIRouter, Depends

from tortoise.contrib.fastapi import HTTPNotFoundError

from src.app.films import schemas, service


imdb_router = APIRouter()


@imdb_router.get('/group/{pk}', response_model=schemas.GetGroup, responses={404: {"model": HTTPNotFoundError}})
async def get_group(pk: int):
    """ Вывод групи """
    return await service.group_s.get(id=pk)


@imdb_router.get('/groups', response_model=List[schemas.GetGroup], responses={404: {"model": HTTPNotFoundError}})
async def get_groups():
    """ Вывод всех груп """
    return await service.group_s.all()


@imdb_router.get('/movie/{pk}', response_model=schemas.Movie, responses={404: {"model": HTTPNotFoundError}})
async def get_movie(pk: int):
    """ Вывод фильма """
    return await service.movie_s.get(id=pk)


@imdb_router.get('/movies/', response_model=Page[schemas.GetFilmReel], responses={404: {"model": HTTPNotFoundError}})
async def get_movies(params: Params = Depends()):
    """ Вывод всех фильмов  """
    movies = await service.movie_s.all(type='Movie')
    return paginate(movies, params)


@imdb_router.get('/tv-series/', response_model=Page[schemas.GetFilmReel], responses={404: {"model": HTTPNotFoundError}})
async def get_tv_series(params: Params = Depends()):
    """ Вывод всех сериалов  """
    movies = await service.movie_s.all(type='TVSeries')
    return paginate(movies, params)
