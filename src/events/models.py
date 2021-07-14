from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Direction(models.Model):
    name = models.CharField('Направление', max_length=128)

    class Meta:
        verbose_name = 'Направление воспитательной работы'
        verbose_name_plural = 'Направления воспитательных работ'

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField('Уровень', max_length=32)

    class Meta:
        verbose_name = 'Уровень мероприятия'
        verbose_name_plural = 'Уровни мероприятий'

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField('Роль', max_length=128)

    class Meta:
        verbose_name = 'Роль СибГУ'
        verbose_name_plural = 'Роли СибГУ'

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField('Формат', max_length=128)

    class Meta:
        verbose_name = 'Формат мероприятия'
        verbose_name_plural = 'Форматы мероприятий'

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField('Название', max_length=128)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Event(models.Model):
    direction = models.ForeignKey(
        Direction,
        models.SET_NULL,
        verbose_name='Направление воспитательной работы',
        null=True,
    )
    name = models.CharField('Название мероприятия', max_length=128)
    free_plan = models.BooleanField('Включить в сводный план', default=False)
    level = models.ForeignKey(Level, models.SET_NULL, verbose_name='Уровень мероприятия', null=True)
    role = models.ForeignKey(Role, models.SET_NULL, verbose_name='Роль СибГУ', null=True)
    format = models.ForeignKey(Format, models.SET_NULL, verbose_name='Формат мероприятия', null=True)
    educational_work_in_opop = models.BooleanField('Воспитательная работа в рамках ОПОП', default=False)
    hours_count = models.PositiveSmallIntegerField('Количество часов', blank=True, null=True)
    educational_work_outside_opop = models.BooleanField('Воспитательная работа за пределами ОПОП', default=True)
    start_date = models.DateField('Дата начала')
    stop_date = models.DateField('Дата окончания', blank=True)
    place = models.CharField('Место проведения', max_length=256)
    coverage_participants_plan = models.PositiveSmallIntegerField('Охват участников (план)')
    number_organizers = models.PositiveSmallIntegerField('Из них организаторов', blank=True, null=True)
    responsible = models.ForeignKey(User, models.SET_NULL, 'my_events', verbose_name='Ответственное лицо', null=True)
    organization = models.ForeignKey(
        Organization,
        models.SET_NULL,
        verbose_name='Ответственное подразделение',
        null=True,
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


class Comment(models.Model):
    author = models.ForeignKey(User, models.SET_NULL, 'comments', null=True, verbose_name='Автор')
    text = models.TextField('Комментарий')
    event = models.ForeignKey(Event, models.CASCADE, 'comments', verbose_name='Мероприятие')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
