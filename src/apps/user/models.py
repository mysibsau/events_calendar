from apps.helpers.models import enum_max_length
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from apps.helpers.models import enum_max_length


class UserRole(models.IntegerChoices):
    author = 0, "Автор"
    moderator = 1, "Модератор"
    administrator = 2, "Администратор"


class Invite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="invites")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="invited_by", null=True, blank=True, default=None
    )
    role = models.IntegerField("Роль", choices=UserRole.choices)


class User(AbstractUser):
    confirmed = models.BooleanField("Подтвержден", default=False)
    role = models.IntegerField("Роль", choices=UserRole.choices, default=UserRole.author)

    def __str__(self):
        return self.get_full_name()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
