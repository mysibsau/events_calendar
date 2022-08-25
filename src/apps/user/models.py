import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserRole(models.IntegerChoices):
    author = 0, "Автор"
    moderator = 1, "Модератор"
    administrator = 2, "Администратор"


class PersonalStatus(models.IntegerChoices):
    student = 0, "Студент"
    staff = 1, "Сотрудник"


class Invite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="invites")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="invited_by", null=True, blank=True, default=None
    )
    role = models.IntegerField("Роль", choices=UserRole.choices)
    status = models.IntegerField("Статус", choices=PersonalStatus.choices, default=PersonalStatus.student)
    position = models.TextField("Должность", blank=True, default="", help_text="Должность или группа")


class User(AbstractUser):
    role = models.IntegerField("Роль", choices=UserRole.choices, default=UserRole.author)
    status = models.IntegerField("Статус", choices=PersonalStatus.choices, default=PersonalStatus.student)
    position = models.TextField("Должность", blank=True, default="", help_text="Должность или группа")
    contact_info = models.TextField("Контактная информация", blank=True, default="", help_text="Контактная информация")

    def __str__(self):
        return self.get_full_name()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
