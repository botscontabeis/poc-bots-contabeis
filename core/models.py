from django.db import models

from .validators import valida_cnpj_ou_cpf, valida_tamanho_cnpj, valida_tamanho_cpf


class Cliente(models.Model):
    razao_social = models.CharField("Razão Social", max_length=255)
    cnpj = models.CharField(
        "CNPJ",
        max_length=14,
        blank=True,
        null=True,
        validators=[valida_tamanho_cnpj],
    )
    cpf = models.CharField(
        "CPF",
        max_length=11,
        blank=True,
        null=True,
        validators=[valida_tamanho_cpf],
    )

    @property
    def cnpj_ou_cpf(self):
        return self.cnpj or self.cpf

    def __str__(self) -> str:
        return f"{self.cnpj_ou_cpf} - {self.razao_social}"

    def clean(self) -> None:
        valida_cnpj_ou_cpf(self)
