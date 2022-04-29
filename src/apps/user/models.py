from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserRole(models.TextChoices):
    default = 'default', 'Обычный пользователь'
    author = 'author', 'Автор'
    moderator = 'moder', 'Модератор'
    administrator = 'admin', 'Администратор'


class User(AbstractUser):
    confirmed = models.BooleanField('Подтвержден', default=False)
    role = models.CharField('Роль', max_length=8, choices=UserRole.choices, default=UserRole.default)

    def __str__(self):
        return self.get_full_name()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
