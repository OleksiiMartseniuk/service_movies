import pytest
from httpx import AsyncClient

from main import app
from src.tests.app.conftest import collection_person


class TestPerson:

    @pytest.mark.asyncio
    async def test_get_person(self):
        await collection_person()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/person/1")
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'id_person': 'id_person_0',
            'name': 'name_0',
            'image': None,
            'as_character': None
        }

    @pytest.mark.parametrize('person', ['writer', 'director', 'star', 'actor'])
    @pytest.mark.asyncio
    async def test_get_list_person_for_film_reel(self, person):
        await collection_person()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/person-list", params={'person': f'{person}', 'id_film_reel': 1})
        assert response.status_code == 200

        assert len(response.json()) == 2
        assert response.json()[0] == {
            'id': 1,
            'id_person': 'id_person_0',
            'name': 'name_0',
            'image': None,
            'as_character': None
        }
