import csv

from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils import timezone

from apps.events.models import Report


def export_as_csv(queryset: QuerySet[Report]) -> HttpResponse:
    meta = queryset.model._meta

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}_{timezone.localtime()}.csv'

    writer = csv.writer(response)
    writer.writerow(field.verbose_name for field in meta.fields)

    for obj in queryset:
        writer.writerow(
            obj.__getattribute__(field.name)
            for field in meta.fields
        )

    return response
