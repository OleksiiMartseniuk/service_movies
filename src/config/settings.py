import os

API_KEY = os.getenv('API_KEY')

NAME_DB = os.getenv('NAME_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')
HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')

DATABASE_URI = os.getenv('DATABASE_URI')

APPS_MODELS = [
    "src.app.films.models",
    "src.app.auth.models",
    "aerich.models"
]

GROUPS_LIST = [
    'Top250Movies',
    'Top250TVs',
    'MostPopularMovies',
    'MostPopularTVs'
]

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
