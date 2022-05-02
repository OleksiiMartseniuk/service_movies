from tortoise import fields, models
from src.app.films.models import FilmReel


class User(models.Model):
    """ Модель Пользователя"""
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=255, unique=True)
    amount_of_time_spent = fields.IntField(default=0)
    movie: fields.ManyToManyRelation[FilmReel] = fields.ManyToManyField(
        'models.FilmReel', related_name='movies', through='user_filmreel_movie'
    )
    tv_series: fields.ManyToManyRelation[FilmReel] = fields.ManyToManyField(
        'models.FilmReel', related_name='tv_series', through='user_filmreel_tv_series'
    )
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    data_join = fields.DatetimeField(auto_now_add=True)
    last_join = fields.DatetimeField(auto_now=True)

    def amount_of_time_spent_plus(self, movie: FilmReel):
        self.movie.add(movie)
        self.amount_of_time_spent += int(movie.runtime_min)

    def amount_of_time_spent_minus(self, movie: FilmReel):
        self.amount_of_time_spent -= int(movie.runtime_min)
        self.movie.remove(movie)

    def __str__(self):
        return self.username
