import os
from docx import Document

from django.http import FileResponse
from docxtpl import DocxTemplate

from apps.events.models import Event


def report_exporter(event: Event) -> FileResponse:
    template = DocxTemplate("/".join(__file__.split("/")[:-1]) + "/template.docx")
    supervisor = "Заместитель директора по ВР" if event.level.name.lower() == "институтский" else "Начальник ОРСП"

    template.render(
        {
            "event_name": event.report.name,
            "organization": event.report.organization.name,
            "date": f'({event.report.start_date_fact} - {event.report.stop_date_fact})',
            "place": event.report.place_fact,
            "level": event.level,
            "description": event.description,
            "links": event.report.links,
            "supervisor": supervisor,
        }
    )
    template.save(f"{event.name}_отчет.docx")
    doc = Document(f"{event.name}_отчет.docx")
    table = doc.tables[0]

    for i, organizator in enumerate(event.report.organizators.all()):
        table.add_row()
        table.cell(i+1, 0).text = str(i+1)
        table.cell(i+1, 1).text = organizator.name
        table.cell(i+1, 2).text = organizator.position
        table.cell(i+1, 3).text = organizator.description

    doc.save(f"{event.name}_отчет.docx")
    response = FileResponse(open(f"{event.name}_отчет.docx", "rb"))
    os.remove(f"{event.name}_отчет.docx")

    return response
