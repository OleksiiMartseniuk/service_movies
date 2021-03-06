from tortoise import fields, models
from enum import Enum

from src.app.person.models import Person


class ModelNameFilmReel(str, Enum):
    movie = "Movie"
    tv_series = "TVSeries"


class Group(models.Model):
    """Група фильмов"""
    title = fields.CharField(max_length=20)
    created = fields.DatetimeField(auto_now_add=True)
    groups: fields.ReverseRelation['FilmReel']

    def __str__(self):
        return self.title


class Genre(models.Model):
    """ Жанры """
    title_key = fields.CharField(max_length=50)
    title_value = fields.CharField(max_length=50)
    genres: fields.ManyToManyRelation['FilmReel']

    def __str__(self):
        return self.title_key


class Country(models.Model):
    """ Страна """
    name_key = fields.CharField(max_length=50)
    name_value = fields.CharField(max_length=50)
    countries: fields.ManyToManyRelation['FilmReel']

    def __str__(self):
        return self.name_key


class Company(models.Model):
    """ Компания """
    id_company = fields.CharField(max_length=15)
    name = fields.CharField(max_length=150)
    companies: fields.ManyToManyRelation['FilmReel']

    def __str__(self):
        return self.id_company


class Language(models.Model):
    """ Язык """
    name_key = fields.CharField(max_length=50)
    name_value = fields.CharField(max_length=50)
    languages: fields.ManyToManyRelation['FilmReel']

    def __str__(self):
        return self.name_key


class BoxOffice(models.Model):
    """ Театральная касса """
    id_movie = fields.CharField(max_length=20)
    budget = fields.CharField(max_length=50, null=True)
    opening_weekend_usa = fields.CharField(max_length=50, null=True)
    gross_usa = fields.CharField(max_length=50, null=True)
    cumulative_worldwide_gross = fields.CharField(max_length=50, null=True)
    box_office: fields.OneToOneRelation['FilmReel']

    def __str__(self):
        return f'BoxOffice -> {self.id_movie}'


class FilmReel(models.Model):
    """ Кино лента """
    id_movie = fields.CharField(max_length=20)
    title = fields.CharField(max_length=255)
    full_title = fields.CharField(max_length=255)
    type = fields.CharField(max_length=20)
    year = fields.CharField(max_length=10)
    image = fields.CharField(max_length=1000)
    release_date = fields.CharField(max_length=10, null=True)
    runtime_min = fields.CharField(max_length=10, null=True)
    runtime_str = fields.CharField(max_length=20, null=True)
    plot = fields.TextField()
    plot_local = fields.TextField()
    plot_local_is_rtl = fields.BooleanField()
    awards = fields.CharField(max_length=200)
    director: fields.ManyToManyRelation[Person] = fields.ManyToManyField(
        'models.Person', related_name='directors', through='filmreel_person_director'
    )
    writer: fields.ManyToManyRelation[Person] = fields.ManyToManyField(
        'models.Person', related_name='writers', through='filmreel_person_writer'
    )
    star: fields.ManyToManyRelation[Person] = fields.ManyToManyField(
        'models.Person', related_name='stars', through='filmreel_person_star'
    )
    actor: fields.ManyToManyRelation[Person] = fields.ManyToManyField(
        'models.Person', related_name='actors', through='filmreel_person_actor'
    )
    genre: fields.ManyToManyRelation[Genre] = fields.ManyToManyField(
        'models.Genre', related_name='genres', through='filmreel_genre'
    )
    company: fields.ManyToManyRelation[Company] = fields.ManyToManyField(
        'models.Company', related_name='companies', through='filmreel_company'
    )
    country: fields.ManyToManyRelation[Country] = fields.ManyToManyField(
        'models.Country', related_name='countries', through='filmreel_country'
    )
    language: fields.ManyToManyRelation[Language] = fields.ManyToManyField(
        'models.Language', related_name='languages', through='filmreel_language'
    )
    content_rating = fields.CharField(max_length=10, null=True)
    imdb_rating = fields.CharField(max_length=100)
    imdd_rating_votes = fields.CharField(max_length=20)
    metacritic_rating = fields.CharField(max_length=10, null=True)
    box_office: fields.OneToOneRelation[BoxOffice] = fields.OneToOneField(
        'models.BoxOffice', related_name='box_office', null=True
    )
    tagline = fields.TextField(null=True)
    rank_top_250 = fields.CharField(max_length=20, null=True)
    creator: fields.ManyToManyRelation[Person] = fields.ManyToManyField(
        'models.Person', related_name='creator', through='filmreel_person_creator'
    )
    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField(
        'models.Group', related_name='groups'
    )

    def __str__(self):
        return self.title
