from django.db import models

from commons.models import BaseModel
from core.models import Cliente


# TODO: mover para models do core
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
    def atualizar_ou_criar(cls, dados):
        fields_map = {
            "Aguardando Leitura": "aguardando_leitura",
            "Aceite Pessoalmente": "aceite_pessoalmente",
            "Recusada Pessoalmente": "recusada_pessoalmente",
            "Cancelada": "cancelada",
            "Lida": "lida",
            "Aceite via DTE": "aceite_via_dte",
            "Recusada via DTE": "recusada_via_dte",
        }

        for d in dados:
            cliente_id = d.pop("cliente")
            cliente = Cliente.objects.get(id=cliente_id)
            fields = cls._mapear_fields(fields_map, d)

            cls.objects.update_or_create(cliente=cliente, defaults=fields)

    @classmethod
    def _mapear_fields(cls, fields_map, dados):
        fields = {}
        for chave_bot, chave_model in fields_map.items():
            if chave_bot in dados:
                fields[chave_model] = dados[chave_bot]

        return fields
