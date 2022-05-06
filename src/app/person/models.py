from tortoise import fields, models
from enum import Enum


class ModelName(str, Enum):
    director = "director"
    writer = "writer"
    star = "star"
    actor = "actor"


class Person(models.Model):
    """ Модель человека """
    id_person = fields.CharField(max_length=15)
    name = fields.CharField(max_length=100)
    image = fields.CharField(max_length=1000, null=True)
    as_character = fields.CharField(max_length=150, null=True)

    def __str__(self):
        return self.id_person
