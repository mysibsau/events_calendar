import os
from docx import Document

from django.http import HttpResponse
from docxtpl import DocxTemplate

from apps.events.models import Event

TEMPLATE_PATH_FILE = os.path.abspath('apps\\helpers\\template.docx')
LIMIT_NAME_FILE_LEN = 99


def report_exporter(event: Event) -> HttpResponse:
    template = DocxTemplate(TEMPLATE_PATH_FILE)
    supervisor = "Заместитель директора по ВР" if event.level.lower() == "институтский" else "Начальник ОРСП"

    template.render(
        {
            "event_name": event.report.name,
            "organization": event.report.organization,
            "date": f'({event.report.start_date_fact} - {event.report.stop_date_fact})',
            "place": event.report.place_fact,
            "level": event.level,
            "description": event.description,
            "count_index": event.report.count_index,
            "links": event.report.links,
            "supervisor": supervisor,
        }
    )

    name_file_report = f"{event.name}_отчет.docx"

    if len(name_file_report) > LIMIT_NAME_FILE_LEN:
        name_file_report = name_file_report[:LIMIT_NAME_FILE_LEN + 1] + '...'

    template.save(name_file_report)
    doc = Document(name_file_report)
    table = doc.tables[0]

    for i, organizator in enumerate(event.report.organizators.all()):
        table.add_row()
        table.cell(i+1, 0).text = str(i+1)
        table.cell(i+1, 1).text = organizator.name
        table.cell(i+1, 2).text = organizator.position
        table.cell(i+1, 3).text = organizator.description

    doc.save(name_file_report)

    with open(name_file_report, "rb") as file:
        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        response["Content-Disposition"] = f"attachment; filename={name_file_report}"

    os.remove(name_file_report)

    return response
