import pytest
import json
from httpx import AsyncClient

from main import app
from src.tests.app.conftest import get_user_token, collection_film_reel
from src.app.auth.models import User
from src.app.films.models import FilmReel


class TestUser:

    @pytest.mark.asyncio
    async def test_read_users_me(self):
        user_token = await get_user_token()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/user/me", headers={'Authorization': f'Bearer {user_token}'})
        assert response.status_code == 200
        test_data = response.json()
        assert test_data['id'] == 1
        assert test_data['username'] == 'test'
        assert test_data['email'] == 'test@test.com'
        assert test_data['amount_of_time_spent'] == 0
        assert test_data['is_active'] is True
        assert test_data['is_superuser'] is False
        assert test_data['first_name'] == 'Test'
        assert test_data['last_name'] == 'TEST'

    @pytest.mark.asyncio
    async def test_users_update(self):
        user_token = await get_user_token()

        user = await User.get(id=1)
        assert user.email == 'test@test.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'TEST'

        data = {
            'first_name': 'test1',
            'last_name': 'TEST1',
            'email': 'user@example.com'
        }
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.put(
                "/user/update",
                data=json.dumps(data),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 200

        user = await User.get(id=1)
        assert user.email == 'user@example.com'
        assert user.first_name == 'test1'
        assert user.last_name == 'TEST1'

    @pytest.mark.asyncio
    async def test_user_viewed_movie(self):
        user_token = await get_user_token()
        await collection_film_reel()

        user = await User.get(id=1)
        assert await user.movie.all().count() == 0
        assert user.amount_of_time_spent == 0

        film_reel = await FilmReel.get(id=2)
        film_reel.runtime_min = 100
        await film_reel.save()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/viewed",
                data=json.dumps({'id_film_reel': 2}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 200
        assert response.json() == {'messages': 'Done'}

        user = await User.get(id=1)
        assert await user.movie.all().count() == 1
        assert user.amount_of_time_spent == 100

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/viewed",
                data=json.dumps({'id_film_reel': 2}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 300
        assert response.json() == {'detail': 'Already added'}

    @pytest.mark.asyncio
    async def test_user_viewed_tv_series(self):
        user_token = await get_user_token()
        await collection_film_reel()

        user = await User.get(id=1)
        assert await user.tv_series.all().count() == 0

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/viewed",
                data=json.dumps({'id_film_reel': 1}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 200
        assert response.json() == {'messages': 'Done'}

        user = await User.get(id=1)
        assert await user.tv_series.all().count() == 1

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/viewed",
                data=json.dumps({'id_film_reel': 1}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 300
        assert response.json() == {'detail': 'Already added'}

    @pytest.mark.asyncio
    async def test_user_cancel_preview_movie(self):
        user_token = await get_user_token()
        await collection_film_reel()

        film_reel = await FilmReel.get(id=2)
        film_reel.runtime_min = 100
        await film_reel.save()

        user = await User.get(id=1)
        user.amount_of_time_spent = 100
        await user.save()
        await user.movie.add(film_reel)
        assert await user.movie.all().count() == 1

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/cancel_viewed",
                data=json.dumps({'id_film_reel': 2}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 200
        assert response.json() == {'messages': 'Done'}

        user = await User.get(id=1)
        assert user.amount_of_time_spent == 0
        assert await user.movie.all().count() == 0

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/cancel_viewed",
                data=json.dumps({'id_film_reel': 2}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 300
        assert response.json() == {'detail': 'Object not found'}

    @pytest.mark.asyncio
    async def test_user_cancel_preview_tv_series(self):
        user_token = await get_user_token()
        await collection_film_reel()

        film_reel = await FilmReel.get(id=1)

        user = await User.get(id=1)
        await user.tv_series.add(film_reel)
        assert await user.tv_series.all().count() == 1

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/cancel_viewed",
                data=json.dumps({'id_film_reel': 1}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 200
        assert response.json() == {'messages': 'Done'}

        assert await user.tv_series.all().count() == 0

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/user/cancel_viewed",
                data=json.dumps({'id_film_reel': 1}),
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 300
        assert response.json() == {'detail': 'Object not found'}

    @pytest.mark.asyncio
    async def test_user_all_viewed_movie(self):
        user_token = await get_user_token()
        await collection_film_reel()

        film_reel_list = await FilmReel.filter(type='Movie')

        user = await User.get(id=1)
        for film_reel in film_reel_list:
            await user.movie.add(film_reel)

        assert await user.movie.all().count() == 5

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                "/user/all_viewed",
                params={'film_reel_type': 'Movie'},
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 200
        assert len(response.json()) == 5
        for film_reel in response.json():
            assert film_reel['type'] == 'Movie'

    @pytest.mark.asyncio
    async def test_user_all_viewed_tv_series(self):
        user_token = await get_user_token()
        await collection_film_reel()

        film_reel_list = await FilmReel.filter(type='TVSeries')

        user = await User.get(id=1)
        for film_reel in film_reel_list:
            await user.tv_series.add(film_reel)

        assert await user.tv_series.all().count() == 5

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                "/user/all_viewed",
                params={'film_reel_type': 'TVSeries'},
                headers={'Authorization': f'Bearer {user_token}'}
            )
        assert response.status_code == 200
        assert len(response.json()) == 5
        for film_reel in response.json():
            assert film_reel['type'] == 'TVSeries'
