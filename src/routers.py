from fastapi import APIRouter
from src.app.films.endpoint import imdb
from src.app.auth import api


films = APIRouter()


films.include_router(imdb.imdb_router, prefix='/imdb', tags=['imdb'])
films.include_router(api.user_router, tags=['user'])
