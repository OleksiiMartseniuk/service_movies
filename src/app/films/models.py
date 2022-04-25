from tortoise import fields, models

from src.app.person.models import Person


class Group(models.Model):
    """Група фильмов"""
    title = fields.CharField(max_length=20)
    created = fields.DatetimeField(auto_now_add=True)
    groups: fields.ReverseRelation['FilmReel']

    def __str__(self):
        return self.title


class Genre(models.Model):
    """ Жанры """
    title = fields.CharField(max_length=50)
    genres: fields.ManyToManyRelation['FilmReel']


class Country(models.Model):
    """ Страна """
    name = fields.CharField(max_length=50)
    countries: fields.ManyToManyRelation['FilmReel']


class Company(models.Model):
    """ Компания """
    id_company = fields.CharField(max_length=15)
    name = fields.CharField(max_length=150)
    companies: fields.ManyToManyRelation['FilmReel']


class Language(models.Model):
    """ Язык """
    name_ua = fields.CharField(max_length=50)
    name_ru = fields.CharField(max_length=50)
    languages: fields.ManyToManyRelation['FilmReel']


class BoxOffice(models.Model):
    """ Театральная касса """
    budget = fields.CharField(max_length=50)
    opening_weekend_usa = fields.CharField(max_length=50)
    gross_usa = fields.CharField(max_length=50)
    cumulative_worldwide_gross = fields.CharField(max_length=50)
    box_office: fields.OneToOneRelation['FilmReel']


class FilmReel(models.Model):
    """ Кино лента """
    id_movie = fields.CharField(max_length=20)
    title = fields.CharField(max_length=255)
    full_title = fields.CharField(max_length=255)
    type = fields.CharField(max_length=20)
    year = fields.CharField(max_length=10)
    image = fields.CharField(max_length=1000)
    release_date = fields.CharField(max_length=10)
    runtime_min = fields.CharField(max_length=10)
    runtime_str = fields.CharField(max_length=20)
    plot = fields.TextField()
    plot_local = fields.TextField()
    plot_local_is_rtl = fields.BooleanField()
    awards = fields.CharField(max_length=50)
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
    content_rating = fields.CharField(max_length=10)
    imdb_rating = fields.CharField(max_length=100)
    imDd_rating_votes = fields.CharField(max_length=20)
    metacritic_rating = fields.CharField(max_length=10)
    box_office: fields.OneToOneRelation[BoxOffice] = fields.OneToOneField(
        'models.BoxOffice', related_name='box_office'
    )
    tagline = fields.CharField(max_length=200)
    rank_top_250 = fields.CharField(max_length=20)
    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField(
        'models.Group', related_name='groups'
    )

    def __str__(self):
        return self.title
