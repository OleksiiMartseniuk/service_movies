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
    model = models.Movie
    get_schema = schemas.GetMovie

    async def all(self, **kwargs) -> List[schemas.GetMovie]:
        return await self.get_schema.from_queryset(self.model.filter(**kwargs))

    async def movie_rang(self, **kwargs) -> schemas.GetMovie:
        movies = await self.model.filter(**kwargs)
        pk = random.randrange(movies[0].id, movies[-1].id)
        return await self.get(id=pk)


movie_s = ServiceMovie()
group_s = ServiceGroup()
