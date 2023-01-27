import uuid
from typing import List, Optional, Set

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserRole(models.IntegerChoices):
    author = 0, "Автор"
    moderator = 1, "Модератор"
    administrator = 2, "Администратор"
    super_admin = 3, "Супер администратор"


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
    creation_date = models.DateField("Дата создания", auto_now_add=True, blank=True)

    @staticmethod
    def get_invites(user: "User") -> List["User"]:
        return User.objects.filter(pk__in=Invite.objects.filter(author=user).values_list("user", flat=True))

    def get_my_invites(self, role: UserRole, user: Optional["User"] = None, result: Set["User"] = None) -> Set["User"]:
        me = user or self
        if not result:
            result = set()
        if me.role == role:
            return {me}
        for user_ in User.get_invites(me):
            user_.get_my_invites(role, result=result)
            result.add(user_)
        return result

    def __str__(self):
        return self.get_full_name()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
