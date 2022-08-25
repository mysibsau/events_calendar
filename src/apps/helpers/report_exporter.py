import os
from docx import Document

from django.http import FileResponse
from docxtpl import DocxTemplate

from apps.events.models import Event


def report_exporter(event_id) -> FileResponse:
    test_data = {"FIO": "Жданов Иван Алексеевич", "INST": "IITK", "ROLE": "Student", "COM": "TEST"}

    data_test = {"DOL": "Куратор", "PER": "123", "ACTV": "123", "DOCS": "Паспорт"}

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
        "description": str(event_data.description),
        "links": str(event_data.links),
        "supervisor": supervisor,
    }

    template.render(context)
    template.save(f"{event_data.name}_отчет.docx")
    doc = Document(f"{event_data.name}_отчет.docx")
    table = doc.tables[0]
    for i in range(1, 4):
        table.add_row()
        table.cell(i, 0).text = str(i)
        table.cell(i, 1).text = f"{test_data['FIO']}, {test_data['INST']}"
        table.cell(i, 2).text = test_data["ROLE"]
        table.cell(i, 3).text = test_data["COM"]
    doc.save(f"{event_data.name}_отчет.docx")
    response = FileResponse(open(f"{event_data.name}_отчет.docx", "rb"))
    os.remove(f"{event_data.name}_отчет.docx")

    return response
