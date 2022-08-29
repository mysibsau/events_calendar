from django.conf import settings
from django.db import models
from django_lifecycle import BEFORE_SAVE, LifecycleModel, hook

from .direction import Direction
from .format import Format
from .level import Level
from .organization import Organization
from .role import Role

User = settings.AUTH_USER_MODEL


class EventStatus(models.TextChoices):
    rejected = 0, "Отклоненно"
    in_process = 1, "В обработке"
    wait_for_report = 2, "В ожидании отчета"
    verified = 3, "Верефицированно"
    rejected_report = 4, "Отчет отклонен"


class Organiztor(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    description = models.TextField()


class EventGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Описание", default="")
    start_date = models.DateField("Дата начала")
    stop_date = models.DateField("Дата окончания", blank=True, null=True)
    author = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, verbose_name="Автор")


fields = [
    "direction",
    "name",
    "free_plan",
    "level",
    "role",
    "format",
    "educational_work_in_opop",
    "hours_count",
    "start_date",
    "stop_date",
    "place",
    "coverage_participants_plan",
    "number_organizers",
    "organization",
    "organizators",
    "coverage_participants_fact",
    "links",
]


class Event(LifecycleModel):
    direction = models.ForeignKey(
        Direction,
        models.SET_NULL,
        verbose_name="Направление воспитательной работы",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Описание", default="")
    name = models.CharField("Название мероприятия", max_length=512)
    status = models.CharField(
        "Статус Мероприятия", max_length=1, choices=EventStatus.choices, default=EventStatus.in_process
    )
    free_plan = models.BooleanField("Включить в сводный план", default=False)
    level = models.ForeignKey(Level, models.SET_NULL, verbose_name="Уровень мероприятия", null=True, blank=True)
    role = models.ForeignKey(Role, models.SET_NULL, verbose_name="Роль СибГУ", null=True, blank=True)
    format = models.ForeignKey(Format, models.SET_NULL, verbose_name="Формат мероприятия", null=True, blank=True)
    educational_work_in_opop = models.BooleanField("Воспитательная работа в рамках ОПОП", default=False)
    hours_count = models.PositiveSmallIntegerField("Количество часов", blank=True, null=True)
    start_date = models.DateField("Дата начала")
    stop_date = models.DateField("Дата окончания", blank=True)
    place = models.CharField("Место проведения", max_length=256)
    coverage_participants_plan = models.PositiveSmallIntegerField("Охват участников (план)")
    number_organizers = models.PositiveSmallIntegerField("Из них организаторов", blank=True, null=True)
    author = models.ForeignKey(User, models.SET_NULL, "my_events", verbose_name="Автор", null=True)
    organization = models.ForeignKey(
        Organization,
        models.SET_NULL,
        verbose_name="Ответственное подразделение",
        null=True,
        blank=True,
    )
    organizators = models.ManyToManyField(Organiztor, null=True, blank=True)
    coverage_participants_fact = models.PositiveSmallIntegerField("Охват участников (факт)", blank=True, null=True)
    links = models.TextField("Ссылки на материалы в интернете о мероприятии (факт)", blank=True)
    verified = models.ForeignKey(
        User, models.SET_NULL, "my_verifications", verbose_name="Кто верифицировал", null=True, blank=True
    )
    verified_date = models.DateField("Дата верификации", blank=True, null=True)
    group = models.ForeignKey(EventGroup, models.SET_NULL, "events", null=True, blank=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    @hook(BEFORE_SAVE, when_any=fields)
    def update_status(self):
        self.status = {
            EventStatus.rejected: EventStatus.in_process,
            EventStatus.rejected_report: EventStatus.wait_for_report,
        }.get(self.status, self.status)

    def verificate(self):
        self.status = {
            EventStatus.wait_for_report: EventStatus.verified,
            EventStatus.in_process: EventStatus.wait_for_report,
        }.get(self.status, self.status)
        self.save()

    def reject(self):
        self.status = {
            EventStatus.in_process: EventStatus.rejected,
            EventStatus.wait_for_report: EventStatus.rejected_report,
        }.get(self.status, self.status)
        self.save()
