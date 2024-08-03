from django.contrib import admin

from .actions import action_consultar_dte, action_debug_task
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    model = Cliente
    list_display = ["cnpj_ou_cpf", "razao_social"]
    search_fields = ["cnpj", "cpf", "razao_social"]
    actions = [action_debug_task, action_consultar_dte]

    def cnpj_ou_cpf(self, obj: Cliente):
        return obj.cnpj_ou_cpf

    cnpj_ou_cpf.short_description = "CNPJ/CPF"
