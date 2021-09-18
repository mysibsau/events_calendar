from django.db import models


class Organization(models.Model):
    name = models.CharField('Название', max_length=128)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name
