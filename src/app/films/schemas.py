from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from src.app.films import models

GetGroup = pydantic_model_creator(models.Group, name="get_group")
GetFilmReel = pydantic_model_creator(models.FilmReel, name="get_film_reel")
GetGenre = pydantic_model_creator(models.Genre, name="get_genre")
GetCountry = pydantic_model_creator(models.Country, name="get_country")
GetCompany = pydantic_model_creator(models.Company, name="get_company")
GetLanguage = pydantic_model_creator(models.Language, name="get_language")
GetBoxOffice = pydantic_model_creator(models.BoxOffice, name="get_box_office")


class Movie(BaseModel):
    film_reel: GetFilmReel
    get_group: GetGroup
    country: GetCountry
    company: GetCompany
    language: GetLanguage
