import os

from django.http import FileResponse
from docxtpl import DocxTemplate

from apps.events.models import Event


def report_exporter(event: Event) -> FileResponse:
    template = DocxTemplate("/".join(__file__.split("/")[:-1]) + "/template.docx")

    supervisor = "Заместитель директора по ВР" if event.level.name.lower() == "институтский" else "Начальник ОРСП"

    template.render(
        {
            "event_name": event.name,
            "organization": event.organization.name,
            "start_date": event.start_date.strftime("%d.%m.%Y"),
            "place": event.place,
            "level": event.level.name,
            "description": event.description,
            "links": event.links,
            "supervisor": supervisor,
        }
    )

    template.save(f"{event.name}_отчет.docx")
    response = FileResponse(open(f"{event.name}_отчет.docx", "rb"))
    os.remove(f"{event.name}_отчет.docx")

    return response
