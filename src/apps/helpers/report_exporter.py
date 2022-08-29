import os
from docx import Document

from django.http import FileResponse
from docxtpl import DocxTemplate

from apps.events.models import Event


def report_exporter(event: Event) -> FileResponse:
    test_data = {"FIO": "Жданов Иван Алексеевич", "INST": "IITK", "ROLE": "Student", "COM": "TEST"}

    data_test = {"DOL": "Куратор", "PER": "123", "ACTV": "123", "DOCS": "Паспорт"}

    template = DocxTemplate("/".join(__file__.split("/")[:-1]) + "/template.docx")

    supervisor = "Заместитель директора по ВР" if event.level.name.lower() == "институтский" else "Начальник ОРСП"

    template.render(
        {
            "event_name": event.name,
            "organization": event.organization.name,
            "date": event.start_date.strftime("%d.%m.%Y"),
            "place": event.place,
            "level": event.level.name,
            "description": event.description,
            "links": event.links,
            "supervisor": supervisor,
        }
    )

    template.save(f"{event.name}_отчет.docx")
    doc = Document(f"{event.name}_отчет.docx")
    table = doc.tables[0]
    for i in range(1, 4):
        table.add_row()
        table.cell(i, 0).text = str(i)
        table.cell(i, 1).text = f"{test_data['FIO']}, {test_data['INST']}"
        table.cell(i, 2).text = test_data["ROLE"]
        table.cell(i, 3).text = test_data["COM"]
    doc.save(f"{event.name}_отчет.docx")
    response = FileResponse(open(f"{event.name}_отчет.docx", "rb"))
    os.remove(f"{event.name}_отчет.docx")

    return response
