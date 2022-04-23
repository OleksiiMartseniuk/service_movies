from fastapi import APIRouter
from src.app.films.endpoint import imdb
from fastapi_pagination import add_pagination

films = APIRouter()
add_pagination(imdb.imdb_router)

films.include_router(imdb.imdb_router, prefix='/imdb', tags=['imdb'])
