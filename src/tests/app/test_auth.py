import json

import pytest
from httpx import AsyncClient

from main import app
from src.app.auth.auth import get_current_user
from src.tests.app.conftest import create_user
from src.app.auth.models import User


class TestAuth:

    @pytest.mark.asyncio
    async def test_login_for_access_token(self):
        user = await create_user()

        data = {
            'username': 'test',
            'password': 'password'
        }
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/token", data=data)
        assert response.status_code == 200
        data_test = response.json()
        access_token = data_test.get('access_token')
        assert data_test['token_type'] == 'bearer'

        user_auth = await get_current_user(access_token)

        assert user == user_auth

    @pytest.mark.asyncio
    async def test_login_for_access_token_error(self):
        await create_user()

        data = {
            'username': 'test1',
            'password': 'test1'
        }
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/token", data=data)

        assert response.status_code == 401
        assert response.json() == {'detail': 'Incorrect username or password'}

    @pytest.mark.asyncio
    async def test_create_user(self):
        assert await User.all().count() == 0

        data = {
            'username': 'Test1',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'user@example.com',
            'hashed_password': 'Password1'
        }

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/user/create", data=json.dumps(data))
        assert response.status_code == 200
        data_test = response.json()
        assert data_test['username'] == 'Test1'
        assert data_test['first_name'] == 'First Name'
        assert data_test['last_name'] == 'Last Name'
        assert data_test['email'] == 'user@example.com'

        assert await User.all().count() == 1

    @pytest.mark.asyncio
    async def test_create_user_error(self):

        data = {
            'username': 'Test1',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'user@example.com',
            'hashed_password': 'Password'
        }
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/user/create", data=json.dumps(data))
        assert response.status_code == 400
        assert response.json() == {'detail': 'Password has invalid format ([A-Z]-[a-z]-d)'}
