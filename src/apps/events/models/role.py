from django.db import models


class Role(models.Model):
    name = models.CharField('Роль', max_length=128)

    class Meta:
        verbose_name = 'Роль СибГУ'
        verbose_name_plural = 'Роли СибГУ'

    def __str__(self):
        return self.name
