from django.contrib import admin

from .models import ConsultaDTE, TaskPartialResult


@admin.register(ConsultaDTE)
class ConsultaDTEAdmin(admin.ModelAdmin):
    list_display = [
        "cliente",
        "aguardando_leitura",
        "lida",
        "atualizado_em",
    ]
    ordering = ["-aguardando_leitura", "-atualizado_em"]
    search_fields = ["cliente__razao_social"]


@admin.register(TaskPartialResult)
class TaskPartialResultAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "criado_em",
        "atualizado_em",
    ]
    ordering = ["-atualizado_em"]
    search_fields = ["task_id"]
