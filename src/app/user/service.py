from typing import List

from fastapi import HTTPException

from src.service.CRUD import ServiceCRUD
from src.app.auth.models import User
from src.app.auth import schemas as schemas_auth
from src.app.films.models import FilmReel, ModelNameFilmReel
from src.app.user import schemas
from src.app.films.schemas import GetFilmReel


class ServiceUser(ServiceCRUD):
    model = User
    model_film_reel = FilmReel
    get_schema = schemas_auth.User

    async def viewed(self, pk: schemas.FilmReelId, current_user: User) -> schemas.Messages:
        """ Добавить в просмотренные """
        film_reel = await self.model_film_reel.get(id=pk.id_film_reel)
        if film_reel.type == 'Movie':
            if film_reel not in await current_user.movie.all():
                await current_user.movie.add(film_reel)
                current_user.amount_of_time_spent += int(film_reel.runtime_min)
                await current_user.save()
            else:
                raise HTTPException(status_code=300, detail="Already added")
        if film_reel.type == 'TVSeries':
            if film_reel not in await current_user.tv_series.all():
                await current_user.tv_series.add(film_reel)
            else:
                raise HTTPException(status_code=300, detail="Already added")
        return schemas.Messages(messages='Done')

    async def cancel_preview(self, pk: schemas.FilmReelId, current_user: User) -> schemas.Messages:
        """ Отменить с просмотренных """
        film_reel = await self.model_film_reel.get(id=pk.id_film_reel)
        if film_reel.type == 'Movie':
            if film_reel in await current_user.movie.all():
                await current_user.movie.remove(film_reel)
                current_user.amount_of_time_spent -= int(film_reel.runtime_min)
                await current_user.save()
            else:
                raise HTTPException(status_code=300, detail="Object not found")
        if film_reel.type == 'TVSeries':
            if film_reel in await current_user.tv_series.all():
                await current_user.tv_series.remove(film_reel)
            else:
                raise HTTPException(status_code=300, detail="Object not found")
        return schemas.Messages(messages='Done')

    async def all_viewed(self, film_reel_type: ModelNameFilmReel, current_user: User) -> List[GetFilmReel]:
        if film_reel_type.value == 'Movie':
            list_film_reel = current_user.movie
        elif film_reel_type.value == 'TVSeries':
            list_film_reel = current_user.tv_series
        else:
            raise HTTPException(status_code=300, detail="Object not found")
        return await GetFilmReel.from_queryset(list_film_reel.all())


user_s = ServiceUser()
