from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.app.person import schemas, service, models

person_router = APIRouter()


@person_router.get('/person/{pk}', response_model=schemas.GetPerson, responses={404: {"model": HTTPNotFoundError}})
async def get_person(pk: int):
    """ Вывод группы """
    return await service.person_s.get(id=pk)


@person_router.get(
    '/person-list',
    response_model=List[schemas.GetPerson],
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_list_person_for_film_reel(person: models.ModelName, id_film_reel: int):
    """ Список группы (director, writer, star, actor) к определеной ленте"""
    return await service.person_s.list_for_film_reel(person, id_film_reel)
