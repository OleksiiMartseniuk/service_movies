from typing import List

from fastapi import HTTPException

from src.app.person import schemas, models
from src.app.films.models import FilmReel
from src.service.CRUD import ServiceCRUD


class ServicePerson(ServiceCRUD):
    get_schema = schemas.GetPerson
    model = models.Person
    model_film = FilmReel

    async def list_for_film_reel(self, person: models.ModelName, id_film_reel: int) -> List[schemas.GetPerson]:
        film_reel = await self.model_film.get(id=id_film_reel)
        if person.value == 'director':
            list_person = film_reel.director
        elif person.value == 'writer':
            list_person = film_reel.writer
        elif person.value == 'star':
            list_person = film_reel.star
        elif person.value == 'actor':
            list_person = film_reel.actor
        else:
            raise HTTPException(status_code=404, detail=f"person not valid")
        return await self.get_schema.from_queryset(list_person.all())


person_s = ServicePerson()
