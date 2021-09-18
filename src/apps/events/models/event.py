from django.conf import settings
from django.db import models

from .direction import Direction
from .format import Format
from .level import Level
from .organization import Organization
from .role import Role

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    direction = models.ForeignKey(
        Direction,
        models.SET_NULL,
        verbose_name='Направление воспитательной работы',
        null=True,
        blank=True,
    )
    name = models.CharField('Название мероприятия', max_length=512)
    free_plan = models.BooleanField('Включить в сводный план', default=False)
    level = models.ForeignKey(Level, models.SET_NULL, verbose_name='Уровень мероприятия', null=True, blank=True)
    role = models.ForeignKey(Role, models.SET_NULL, verbose_name='Роль СибГУ', null=True, blank=True)
    format = models.ForeignKey(Format, models.SET_NULL, verbose_name='Формат мероприятия', null=True, blank=True)
    educational_work_in_opop = models.BooleanField('Воспитательная работа в рамках ОПОП', default=False)
    hours_count = models.PositiveSmallIntegerField('Количество часов', blank=True, null=True)
    educational_work_outside_opop = models.BooleanField('Воспитательная работа за пределами ОПОП', default=True)
    start_date = models.DateField('Дата начала')
    stop_date = models.DateField('Дата окончания', blank=True)
    place = models.CharField('Место проведения', max_length=256)
    coverage_participants_plan = models.PositiveSmallIntegerField('Охват участников (план)')
    number_organizers = models.PositiveSmallIntegerField('Из них организаторов', blank=True, null=True)
    responsible = models.CharField('Ответсвенное лицо', max_length=512)
    position = models.CharField('Должность', max_length=512, blank=True)
    author = models.ForeignKey(User, models.SET_NULL, 'my_events', verbose_name='Автор', null=True)
    organization = models.ForeignKey(
        Organization,
        models.SET_NULL,
        verbose_name='Ответственное подразделение',
        null=True,
        blank=True,
    )
    coverage_participants_fact = models.PositiveSmallIntegerField('Охват участников (факт)', blank=True, null=True)
    links = models.TextField('Ссылки на материалы в интернете о мероприятии (факт)', blank=True)
    verified = models.ForeignKey(
        User,
        models.SET_NULL,
        'my_verifications',
        verbose_name='Кто верифицировал',
        null=True,
        blank=True
    )
    verified_date = models.DateField('Дата верификации', blank=True, null=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return f'{self.name} ({self.start_date})'
