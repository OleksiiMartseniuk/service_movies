from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.config import settings

from src.routers import films

app = FastAPI()

app.include_router(films)

register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)
