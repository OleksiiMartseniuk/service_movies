import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

API_KEY = os.getenv('API_KEY')

NAME_DB = os.getenv('POSTGRES_DB')
USER_DB = os.getenv('POSTGRES_USER')
PASSWORD_DB = os.getenv('POSTGRES_PASSWORD')
HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')

DATABASE_URI = f'postgres://{USER_DB}:{PASSWORD_DB}@{HOST_DB}/{NAME_DB}'
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

PATH_GROUP_FILE = os.path.join(DATA_IMDB_DIR, 'group_movies.json')
PATH_MOVIES_FILE = os.path.join(DATA_IMDB_DIR, 'movies.json')

TABLES_LIST = [
    'filmreel_person_creator', 'filmreel_person_star', 'filmreel_person_actor',
    'filmreel_person_director', 'filmreel_person_writer', 'filmreel_company',
    'filmreel_country', 'filmreel_genre', 'filmreel_language',
    'boxoffice', 'company', 'country',
    'filmreel', 'genre', 'group',
    'language', 'person'
]
