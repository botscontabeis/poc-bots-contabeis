from django.db import models

from commons.models import BaseModel
from core.models import Cliente


class TaskPartialResult(BaseModel):
    task_id = models.UUIDField()
    clientes_finalizados = models.JSONField("Cliente com execução finalizada", default=list)

    def __str__(self):
        return f"Resultado parcial da task {self.task_id}"


class ConsultaDTE(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    aguardando_leitura = models.SmallIntegerField(default=0)
    aceite_pessoalmente = models.SmallIntegerField(default=0)
    recusada_pessoalmente = models.SmallIntegerField(default=0)
    cancelada = models.SmallIntegerField(default=0)
    lida = models.SmallIntegerField(default=0)
    aceite_via_dte = models.SmallIntegerField(default=0)
    recusada_via_dte = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Consulta DTE"
        verbose_name_plural = "Consultas DTE"

    def __str__(self) -> str:
        return f"Consulta DTE {self.cliente.razao_social} - {self.aguardando_leitura} mensagens não lidas"

    @classmethod
    def atualizar_ou_criar_resultados(cls, resultados_bot):
        fields_map = {
            "Aguardando Leitura": "aguardando_leitura",
            "Aceite Pessoalmente": "aceite_pessoalmente",
            "Recusada Pessoalmente": "recusada_pessoalmente",
            "Cancelada": "cancelada",
            "Lida": "lida",
            "Aceite via DTE": "aceite_via_dte",
            "Recusada via DTE": "recusada_via_dte",
        }

        for resultado in resultados_bot:
            cliente_id = resultado.pop("cliente")
            cliente = Cliente.objects.get(id=cliente_id)
            fields = {}
            for chave_bot, chave_model in fields_map.items():
                if chave_bot in resultado:
                    fields[chave_model] = resultado[chave_bot]

            cls.objects.update_or_create(cliente=cliente, defaults=fields)
