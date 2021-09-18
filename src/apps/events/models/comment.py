from django.conf import settings
from django.db import models
from .event import Event

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    author = models.ForeignKey(User, models.SET_NULL, 'comments', null=True, verbose_name='Автор')
    text = models.TextField('Комментарий')
    event = models.ForeignKey(Event, models.CASCADE, 'comments', verbose_name='Мероприятие')
    date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']
