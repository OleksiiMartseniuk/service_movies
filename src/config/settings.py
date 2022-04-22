import os

DATABASE_URI = os.getenv('DATABASE_URI')

APPS_MODELS = [
    "src.database.models",
    "aerich.models"
]
