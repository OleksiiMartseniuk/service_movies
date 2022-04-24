from tortoise import fields, models


class User(models.Model):
    """ Модель Пользователя"""
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self):
        return self.username
