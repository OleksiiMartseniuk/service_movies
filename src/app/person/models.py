from tortoise import fields, models


class Person(models.Model):
    """ Модель человека """
    id_person = fields.CharField(max_length=15)
    name = fields.CharField(max_length=100)
    image = fields.CharField(max_length=1000, null=True)
    as_character = fields.CharField(max_length=150, null=True)
    # directors: fields.ManyToManyRelation['FilmReel']
    # writers: fields.ManyToManyRelation['FilmReel']
    # stars: fields.ManyToManyRelation['FilmReel']
    # actors: fields.ManyToManyRelation['FilmReel']

    def __str__(self):
        return self.id_person
