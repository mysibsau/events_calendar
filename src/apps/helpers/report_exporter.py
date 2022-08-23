from docxtpl import DocxTemplate
from apps.events.models import Event


def report_exporter(event_id):
    event_data = Event.objects.first()
    template = DocxTemplate("template.docx")
    context = {
        "event_name": str(event_data.name)
    }

    template.render(context)
    template.save("new_generated.docx")
