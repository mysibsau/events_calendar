from django.conf import settings
from django.db import models
from django_lifecycle import BEFORE_SAVE, LifecycleModel, hook

from .direction import Direction
from .format import Format
from .level import Level
from .organization import Organization
from .role import Role
from .organizator_role import OrganizatorRole


User = settings.AUTH_USER_MODEL


class EventStatus(models.TextChoices):
    rejected = 0, "Отклоненно"
    in_process = 1, "В обработке"
    wait_for_report = 2, "В ожидании отчета"
    verified = 3, "Верефицированно"
    rejected_report = 4, "Отчет отклонен"
    wait_for_report_verified = 5, "В ожидании верефикации отчета"


class Organiztor(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField()


class Report(models.Model):
    count_index = models.TextField(verbose_name="Колличественный показатель", default="")
    name = models.CharField("Название мероприятия", max_length=512)
    start_date_fact = models.DateField("Дата начала Факт.")
    stop_date_fact = models.DateField("Дата конца Факт.")
    place_fact = models.CharField(max_length=512, verbose_name="Место проведения факт.")
    coverage_participants_fact = models.PositiveSmallIntegerField("Охват участников (факт.)", blank=True, null=True)
    links = models.TextField("Ссылки на материалы в интернете о мероприятии (факт.)", blank=True)
    organizators = models.ManyToManyField(Organiztor, null=True, blank=True, verbose_name="Организаторы")
    organization = models.ForeignKey(
        Organization,
        models.SET_NULL,
        verbose_name="Ответственное подразделение",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Описание", default="")


class EventGroup(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, blank=True, null=True, verbose_name="Автор", on_delete=models.CASCADE)


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
    direction = models.CharField(max_length=256, verbose_name="Направление воспитательных работ", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", default="")
    name = models.CharField("Название мероприятия", max_length=512)
    status = models.CharField(
        "Статус Мероприятия", max_length=1, choices=EventStatus.choices, default=EventStatus.in_process
    )
    free_plan = models.BooleanField("Включить в сводный план", default=False)
    level = models.CharField(max_length=256, verbose_name="Уровень мероприятия", null=True, blank=True)
    role = models.CharField(max_length=256, verbose_name="Роль СибГУ", null=True, blank=True)
    format = models.CharField(max_length=256, verbose_name="Формат мероприятия", null=True, blank=True)
    educational_work_in_opop = models.BooleanField("Воспитательная работа в рамках ОПОП", default=False)
    hours_count = models.PositiveSmallIntegerField("Количество часов", blank=True, null=True)
    start_date = models.DateField("Дата начала")
    stop_date = models.DateField("Дата окончания", blank=True)
    place = models.CharField("Место проведения", max_length=256)
    coverage_participants_plan = models.PositiveSmallIntegerField("Охват участников (план)")
    number_organizers = models.PositiveSmallIntegerField("Из них организаторов", blank=True, null=True)
    author = models.ForeignKey(User, models.SET_NULL, "my_events", verbose_name="Автор", null=True)
    organization = models.CharField(
        max_length=256,
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
    report = models.ForeignKey(Report, models.SET_NULL, 'event', null=True, blank=True)
    comment = models.TextField("Комментарий", null=True, blank=True)
    original_author = models.CharField(max_length=256, verbose_name="Изначальный автор", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    def verificate(self):
        self.status = {
            EventStatus.in_process: EventStatus.wait_for_report,
            EventStatus.wait_for_report: EventStatus.wait_for_report_verified,
            EventStatus.wait_for_report_verified: EventStatus.verified
        }.get(self.status, self.status)

        if self.status == EventStatus.verified:
            self.start_date = self.report.start_date_fact
            self.stop_date = self.report.stop_date_fact
            
        self.save()

    def reject(self, comment):
        self.status = {
            EventStatus.in_process: EventStatus.rejected,
            EventStatus.wait_for_report: EventStatus.rejected_report,
            EventStatus.wait_for_report_verified: EventStatus.rejected_report,
        }.get(self.status, EventStatus.in_process)

        self.comment = comment
        self.save()
