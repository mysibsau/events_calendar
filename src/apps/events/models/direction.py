from django.db import models


class Direction(models.Model):
    name = models.CharField('Направление', max_length=128)

    class Meta:
        verbose_name = 'Направление воспитательной работы'
        verbose_name_plural = 'Направления воспитательных работ'

    def __str__(self):
        return self.name
