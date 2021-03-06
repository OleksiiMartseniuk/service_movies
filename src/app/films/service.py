import random
from typing import List

from src.app.films import schemas, models
from src.service.CRUD import ServiceCRUD


class ServiceGroup(ServiceCRUD):
    model = models.Group
    get_schema = schemas.GetGroup

    async def all(self) -> List[schemas.GetGroup]:
        return await self.get_schema.from_queryset(self.model.all())


class ServiceMovie(ServiceCRUD):
    model = models.FilmReel
    get_schema = schemas.Movie
    all_schema = schemas.GetFilmReel

    async def all(self, **kwargs) -> List[schemas.GetFilmReel]:
        return await self.all_schema.from_queryset(self.model.filter(**kwargs).order_by('id'))

    async def range_film_reel(self, **kwargs) -> schemas.GetFilmReel:
        film_reel_list = await self.model.filter(**kwargs)
        film_reel = random.choice(film_reel_list)
        return await self.all_schema.from_tortoise_orm(film_reel)


movie_s = ServiceMovie()
group_s = ServiceGroup()
