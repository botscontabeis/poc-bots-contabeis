from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from bots.models import ConsultaDTE
from bots.constants import RETRY_COUNTDOWN
from ..notifications.emails.daily_reports import send_daily_report_consulta_dte


logger = get_task_logger(__name__)


@shared_task(bind=True, acks_late=True)
def task_send_daily_report_consulta_dte(self):
    # TODO: melhorar aquisição dos dados, relacionando as consultas aos destinatários correspondentes

    try:
        logger.info("Iniciando task Enviar Relatório Diário de Consulta DTE")

        logger.info("Buscando consultas aguardando leitura")
        consultas = ConsultaDTE.get_aguardando_leitura()

        logger.info("Buscando destinatários")
        destinatarios = (
            get_user_model().objects.filter(is_active=True, email__isnull=False).values_list("email", flat=True)
        )

        logger.info("Enviando email com relatório diário de consultas DTE")
        send_daily_report_consulta_dte(consultas, destinatarios)

        logger.info("Finalizando task Enviar Relatório Diário de Consulta DTE")

    except Exception as e:
        logger.exception("Erro durante execução da task Enviar Relatório Diário de Consulta DTE")
        raise self.retry(exc=e, countdown=RETRY_COUNTDOWN)
