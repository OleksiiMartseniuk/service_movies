from tortoise.contrib.pydantic import pydantic_model_creator
from src.database import models

GetGroup = pydantic_model_creator(models.Group, name="get_group")
GetMovie = pydantic_model_creator(models.Movie, name="get_movie")
