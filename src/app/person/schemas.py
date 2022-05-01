from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.person import models


GetPerson = pydantic_model_creator(models.Person, name="get_person")
