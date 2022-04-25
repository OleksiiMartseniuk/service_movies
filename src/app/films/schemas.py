from tortoise.contrib.pydantic import pydantic_model_creator
from src.app.films import models

GetGroup = pydantic_model_creator(models.Group, name="get_group")
GetFilmReel = pydantic_model_creator(models.FilmReel, name="get_film_reel")
