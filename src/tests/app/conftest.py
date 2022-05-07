import asyncio

import pytest
from tortoise import Tortoise
from src.config import settings
from src.app.films.models import Group, FilmReel
from src.app.person.models import Person


async def collection_film_reel():
    """ Заполнения данных FilmReel and Group """
    for i in range(2):
        await Group.create(title=f'group_test_{i}')

    for i in range(10):
        await FilmReel.create(
            id_movie=f'id_movie_{i}',
            title=f'title_{i}',
            full_title=f'full_title_{i}',
            type='Movie' if i % 2 else 'TVSeries',
            year=f'year_{i}',
            image=f'image_{i}',
            plot=f'plot_{i}',
            plot_local=f'plot_local_{i}',
            plot_local_is_rtl=True,
            awards=f'awards_{i}',
            imdb_rating=f'imdb_rating_{i}',
            imdd_rating_votes=f'imdd_rating_votes_{i}',
            group_id=1 if i % 2 else 2
        )


async def collection_person():
    """ Заполнения Person к FilmReel """
    await collection_film_reel()

    pk = 1
    for i in range(20):
        person = await Person.create(id_person=f'id_person_{i}', name=f'name_{i}')
        film_reel = await FilmReel.get(id=pk)

        await film_reel.director.add(person)
        await film_reel.writer.add(person)
        await film_reel.star.add(person)
        await film_reel.actor.add(person)
        if i % 2:
            pk += 1


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": settings.APPS_MODELS_TEST}, _create_db=create_db
    )
    if schemas:
        await Tortoise.generate_schemas()


async def init(db_url: str = settings.DATABASE_TEST_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()
