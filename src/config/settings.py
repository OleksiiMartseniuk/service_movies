import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

API_KEY = os.getenv('API_KEY')

NAME_DB = os.getenv('NAME_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')
HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')

DATABASE_URI = os.getenv('DATABASE_URI')
DATABASE_TEST_URL = 'sqlite://:memory:'

ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:4200/",
    "http://localhost:8080/"
]

APPS_MODELS_TEST = [
    "src.app.films.models",
    "src.app.auth.models",
    "src.app.person.models",
]

APPS_MODELS = [
    "src.app.films.models",
    "src.app.auth.models",
    "src.app.person.models",
    "aerich.models"
]

GROUPS_LIST = [
    'Top250Movies',
    'Top250TVs',
]

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATA_IMDB_DIR = os.path.join(BASE_DIR, 'src/service/imdb/data')
DATA_IMDB_DIR_TEST = os.path.join(BASE_DIR, 'src/tests/write_json/data_test')

PATH_GROUP_FILE = os.path.join(DATA_IMDB_DIR, 'group_movies.json')
PATH_MOVIES_FILE = os.path.join(DATA_IMDB_DIR, 'movies.json')

PATH_GROUP_FILE_TEST = os.path.join(DATA_IMDB_DIR_TEST, 'group_movies_test.json')
PATH_MOVIES_FILE_TEST = os.path.join(DATA_IMDB_DIR_TEST, 'movies_test.json')
