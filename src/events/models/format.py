from django.db import models


class Format(models.Model):
    name = models.CharField('Формат', max_length=128)

    class Meta:
        verbose_name = 'Формат мероприятия'
        verbose_name_plural = 'Форматы мероприятий'

    def __str__(self):
        return self.name
