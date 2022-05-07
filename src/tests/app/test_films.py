import pytest

from httpx import AsyncClient

from main import app

from src.tests.app.conftest import collection_film_reel


class TestFilms:

    @pytest.mark.asyncio
    async def test_get_group(self):
        await collection_film_reel()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/imdb/group/1", )

        assert response.status_code == 200
        test_data = response.json()
        assert test_data['id'] == 1
        assert test_data['title'] == 'group_test_0'

    @pytest.mark.asyncio
    async def test_get_groups(self):
        await collection_film_reel()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/imdb/groups", )

        assert response.status_code == 200
        test_data = response.json()
        for id, item in enumerate(test_data):
            assert item['id'] == id + 1
            assert item['title'] == f'group_test_{id}'

    @pytest.mark.asyncio
    async def test_get_movie(self):
        await collection_film_reel()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/imdb/movie/1", )

        assert response.status_code == 200
        test_data = response.json()

        assert test_data['id'] == 1
        assert test_data['id_movie'] == 'id_movie_0'
        assert test_data['title'] == 'title_0'
        assert test_data['full_title'] == 'full_title_0'
        assert test_data['type'] == 'TVSeries'
        assert test_data['year'] == 'year_0'
        assert test_data['image'] == 'image_0'
        assert test_data['release_date'] is None
        assert test_data['runtime_min'] is None
        assert test_data['runtime_str'] is None
        assert test_data['plot'] == 'plot_0'
        assert test_data['plot_local'] == 'plot_local_0'
        assert test_data['plot_local_is_rtl'] is True
        assert test_data['awards'] == 'awards_0'
        assert test_data['content_rating'] is None
        assert test_data['imdd_rating_votes'] == 'imdd_rating_votes_0'
        assert test_data['metacritic_rating'] is None
        assert test_data['tagline'] is None
        assert test_data['director'] == []
        assert test_data['writer'] == []
        assert test_data['star'] == []
        assert test_data['actor'] == []
        assert test_data['genre'] == []
        assert test_data['country'] == []
        assert test_data['company'] == []
        assert test_data['language'] == []
        assert test_data['group']['id'] == 2
        assert test_data['group']['title'] == 'group_test_1'
        assert test_data['box_office'] is None

    @pytest.mark.parametrize('type_name, url_path', [('Movie', 'movies'), ('TVSeries', 'tv-series')])
    @pytest.mark.asyncio
    async def test_get_all(self, type_name, url_path):
        await collection_film_reel()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/imdb/{url_path}", params={'page': 1, 'size': 50})

        assert response.status_code == 200
        test_data = response.json()
        assert len(test_data['items']) == test_data['total']
        for item in test_data['items']:
            assert item['type'] == type_name

    @pytest.mark.parametrize('type_name', ['Movie', 'TVSeries'])
    @pytest.mark.asyncio
    async def test_range_film_reel(self, type_name):
        await collection_film_reel()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"imdb/range/{type_name}")

        assert response.status_code == 200
        test_data = response.json()

        assert test_data['type'] == type_name
