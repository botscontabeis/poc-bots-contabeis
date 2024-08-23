from typing import Iterable
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from bots.models import ConsultaDTE


def send_daily_report_consulta_dte(consultas: Iterable[ConsultaDTE], destinatarios: list[str]):
    subject = "Consulta DTE - Relatório Diário"
    body = render_to_string("emails/reports/daily_report_consulta_dte.html", {"consultas": consultas})
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, destinatarios)
    email.content_subtype = "html"
    email.send()
