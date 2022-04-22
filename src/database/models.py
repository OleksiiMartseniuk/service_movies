from tortoise import fields, models


class Group(models.Model):
    """Група фильмов"""
    title = fields.CharField(max_length=20)
    created = fields.DatetimeField(auto_now_add=True)
    groups: fields.ReverseRelation['Movie']

    def __str__(self):
        return self.title


class Movie(models.Model):
    """Фильм"""
    id_movie = fields.CharField(max_length=20)
    rank = fields.IntField()
    title = fields.CharField(max_length=50)
    full_title = fields.CharField(max_length=100)
    year = fields.CharField(max_length=10)
    image = fields.CharField(max_length=1000)
    crew = fields.CharField(max_length=100)
    imDbRating = fields.CharField(max_length=100)
    imDbRatingCount = fields.IntField()
    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField('models.Group', related_name='groups')

    def __str__(self):
        return self.title
