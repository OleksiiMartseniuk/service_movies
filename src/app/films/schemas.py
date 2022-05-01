from typing import List, Optional

from tortoise.contrib.pydantic import pydantic_model_creator
from src.app.films import models
from src.app.person.schemas import GetPerson

GetGroup = pydantic_model_creator(models.Group, name="get_group")
GetFilmReel = pydantic_model_creator(models.FilmReel, name="get_film_reel")
GetGenre = pydantic_model_creator(models.Genre, name="get_genre")
GetCountry = pydantic_model_creator(models.Country, name="get_country")
GetCompany = pydantic_model_creator(models.Company, name="get_company")
GetLanguage = pydantic_model_creator(models.Language, name="get_language")
GetBoxOffice = pydantic_model_creator(models.BoxOffice, name="get_box_office")


class Movie(GetFilmReel):
    director: List[GetPerson] = []
    writer: List[GetPerson] = []
    star: List[GetPerson] = []
    actor: List[GetPerson] = []
    genre: List[GetGenre] = []
    country:  List[GetCountry] = []
    company:  List[GetCompany] = []
    language:  List[GetLanguage] = []
    group: GetGroup
    box_office: Optional[GetBoxOffice] = None
