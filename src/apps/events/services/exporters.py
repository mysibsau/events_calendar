import csv

from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils import timezone

from apps.events.models import Event


def export_as_csv(queryset: QuerySet[Event]) -> HttpResponse:
    headers = [
        'Направление',
        'Название',
        'Уровень',
        'Работа в рамках ОПОП',
        'Кол-во часов',
        'Формат',
        'Переод проведения',
        'Место проведения',
        'Фактический охват участников',
        'Ссылки на материалы СМИ',
        'ФИО',
        'Должность',
        'Контактные данные'
    ]

    meta = queryset.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}_{timezone.localtime()}.csv'

    writer = csv.writer(response)
    writer.writerow(field for field in headers)

    for event in queryset:
        writer.writerow(
            [
                event.direction,
                event.name,
                event.level,
                event.educational_work_in_opop,
                event.hours_count,
                event.format,
                f"{event.start_date} -- {event.stop_date}",
                event.report.place_fact,
                event.report.coverage_participants_fact,
                event.report.links,
                event.author,
                event.author.position,
                event.author.contact_info

            ]
        )

    return response
