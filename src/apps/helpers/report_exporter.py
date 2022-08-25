import os

from django.http import FileResponse
from docxtpl import DocxTemplate

from apps.events.models import Event


def report_exporter(event_id) -> FileResponse:
    event_data = Event.objects.filter(id__in=event_id).first()
    template = DocxTemplate("/".join(__file__.split("/")[:-1]) + "/template.docx")
    supervisor = "Начальник ОРСП"

    if event_data.level.name.lower() == "институтский":
        supervisor = "Заместитель директора по ВР"

    context = {
        "event_name": str(event_data.name),
        "organization": str(event_data.organization),
        "start_date": str(event_data.start_date),
        "place": str(event_data.place),
        "level": str(event_data.level),
        "description": "Описание",
        "links": str(event_data.links),
        "supervisor": supervisor,
    }

    template.render(context)

    template.save(f"{event_data.name}_отчет.docx")
    response = FileResponse(open(f"{event_data.name}_отчет.docx", "rb"))
    os.remove(f"{event_data.name}_отчет.docx")

    return response
