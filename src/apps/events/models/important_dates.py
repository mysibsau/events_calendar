from django.db import models
from apps.events.models.event import Event


class ImportantDate(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    date = models.DateTimeField(verbose_name='Дата')
    event = models.ForeignKey(
        Event,
        models.CASCADE,
        verbose_name='Мероприятие',
        related_name='important_dates'
    )

    def __str__(self) -> str:
        return f'{self.event}[{self.name}]'

    class Meta:
        verbose_name = 'Ключевая дата'
        verbose_name_plural = 'Ключевые даты'
