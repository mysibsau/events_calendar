import os

from docxtpl import DocxTemplate

from apps.events.models import Event


def report_exporter(event_id):
    event_data = Event.objects.first()
    template = DocxTemplate("/".join(__file__.split("/")[:-1]) + "/template.docx")
    context = {"event_name": str(event_data.name)}

    template.render(context)
    template.save("new_generated.docx")
