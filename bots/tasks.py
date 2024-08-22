from celery import shared_task
from celery.utils.log import get_task_logger
from decouple import config
from django.db import transaction

from core.models import Cliente

from .core.consulta_dte import ConsultaDteBot
from .external.captchas.resolvers import AntiCaptchaOfficialCaptchaResolver
from .models import ConsultaDTE, TaskPartialResult

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    retry_backoff=True,
    retry_kwargs={"max_retries": 3, "countdown": 3},
)
def task_consultar_dte(self, cliente_ids: list[str] = []):
    try:
        task_id = self.request.id
        logger.info("Iniciando task Consultar DTE")

        partial_result, _ = TaskPartialResult.objects.get_or_create(task_id=task_id)

        clientes = Cliente.objects.all()
        if cliente_ids:
            clientes = clientes.filter(id__in=cliente_ids)
        # Filtrar clientes que ainda não foram processados
        clientes = clientes.exclude(id__in=partial_result.clientes_finalizados)

        captcha_resolver = AntiCaptchaOfficialCaptchaResolver(config("CAPTCHA_RESOLVER_API_KEY"))
        bot = ConsultaDteBot(clientes, captcha_resolver)

        resultados, erro = bot.executar()

        # Atualizar TaskPartialResult com os clientes processados
        with transaction.atomic():
            partial_result.clientes_finalizados.extend([res["cliente"] for res in resultados])
            partial_result.save()

        # Atualizar resultados no banco de dados
        ConsultaDTE.atualizar_ou_criar(resultados)

        if erro:
            raise erro

        # Deletar o TaskPartialResult se a task foi concluída com sucesso
        TaskPartialResult.objects.filter(task_id=task_id).delete()

        logger.info("Finalizando task Consultar DTE")
        return f"{len(resultados)} empresas consultadas"

    except Exception as e:
        logger.warning(f"Erro durante execução da task Consultar DTE: {str(e)}")
        raise self.retry(exc=e)
