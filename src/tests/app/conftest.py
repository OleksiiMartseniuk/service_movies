import asyncio

import pytest
from tortoise import Tortoise
from src.config import settings


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": settings.APPS_MODELS}, _create_db=create_db
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
