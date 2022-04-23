from typing import List

from src.database import models
from src.app.films import schemas
from src.service.CRUD import ServiceCRUD


class ServiceGroup(ServiceCRUD):
    model = models.Group
    get_schema = schemas.GetGroup

    async def all(self):
        return await self.get_schema.from_queryset(self.model.all())


class ServiceMovie(ServiceCRUD):
    model = models.Movie
    get_schema = schemas.GetMovie

    async def all(self, **kwargs) -> List[schemas.GetMovie]:
        return await self.get_schema.from_queryset(self.model.filter(**kwargs))


movie_s = ServiceMovie()
group_s = ServiceGroup()
