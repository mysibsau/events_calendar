import os

from django.http import HttpResponse
from docxtpl import DocxTemplate

from apps.events.models import Event

TEMPLATE_PATH_FILE = "/".join(__file__.split("/")[:-1]) + "/template.docx"  # Linux
# TEMPLATE_PATH_FILE = os.path.abspath('apps\\helpers\\template.docx')  # Windows
LIMIT_NAME_FILE_LEN = 99


def report_exporter(event: Event) -> HttpResponse:
    template = DocxTemplate(TEMPLATE_PATH_FILE)
    supervisor = "Заместитель директора по ВР" if event.level.lower() == "институтский" else "Руководитель ЦСО"

    table = []
    for count, organizer in enumerate(event.report.organizators.all()):
        human = {'id': str(count + 1),
                 'name': organizer.name,
                 'position': organizer.position,
                 'description': organizer.description
                 }
        table.append(human)

    template.render(
        {
            "event_name": event.report.name,
            "organization": event.report.organization,
            "date": f'{event.report.start_date_fact} - {event.report.stop_date_fact}',
            "place": event.report.place_fact,
            "level": event.level,
            "description": event.description,
            "count_index": event.report.count_index,
            "links": event.report.links,
            "supervisor": supervisor,
            'table': table,
        }
    )

    name_file_report = f"{event.name}_отчет.docx"

    if len(name_file_report) > LIMIT_NAME_FILE_LEN:
        name_file_report = name_file_report[:LIMIT_NAME_FILE_LEN + 1] + '...'

    template.save(name_file_report)

    with open(name_file_report, "rb") as file:
        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        response["Content-Disposition"] = f"attachment; filename={name_file_report}"

    os.remove(name_file_report)

    return response
