from fastapi import APIRouter
from src.app.films.endpoint import imdb
from src.app.auth import api as api_auth
from src.app.person import api as api_person
from src.app.user import api as api_user


films = APIRouter()


films.include_router(imdb.imdb_router, prefix='/imdb', tags=['imdb'])
films.include_router(api_auth.user_router, tags=['auth'])
films.include_router(api_person.person_router, tags=['person'])
films.include_router(api_user.user_router, tags=['user'])
