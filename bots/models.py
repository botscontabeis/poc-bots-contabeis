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
        return f"{self.cliente} - {self.aguardando_leitura} mensagens não lidas"

    @classmethod
    def atualizar_ou_criar(cls, dados: list[dict[str, any]]):
        fields_map = {
            "Aguardando Leitura": "aguardando_leitura",
            "Aceite Pessoalmente": "aceite_pessoalmente",
            "Recusada Pessoalmente": "recusada_pessoalmente",
            "Cancelada": "cancelada",
            "Lida": "lida",
            "Aceite via DTE": "aceite_via_dte",
            "Recusada via DTE": "recusada_via_dte",
        }

        consultas = []
        for d in dados:
            cliente_id = d.pop("cliente")
            cliente = Cliente.objects.get(id=cliente_id)
            fields = cls._mapear_fields(fields_map, d)

            consulta, _ = cls.objects.update_or_create(cliente=cliente, defaults=fields)
            consultas.append(consulta)

        return consultas

    @classmethod
    def _mapear_fields(cls, fields_map: dict[str, str], dados: dict[str, any]) -> dict:
        fields = {}
        for chave_bot, chave_model in fields_map.items():
            if chave_bot in dados:
                fields[chave_model] = dados[chave_bot]

        return fields

    @classmethod
    def get_aguardando_leitura(cls):
        return cls.objects.filter(aguardando_leitura__gt=0)
