from django.db import models


class OrganizatorRole(models.Model):
    name = models.CharField("Роль организатора", max_length=128)

    class Meta:
        verbose_name = 'Роль организатора'
        verbose_name_plural = 'Роли организаторов'

    def __str__(self):
        return self.name
