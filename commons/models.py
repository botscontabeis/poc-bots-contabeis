from django.db import models


class BaseModel(models.Model):
    criado_em = models.DateTimeField("Criando em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        abstract = True
