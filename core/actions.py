from django.contrib import admin

from bots.tasks import task_consultar_dte
from core.tasks import debug_task


@admin.action(description="Executar Debug Task")
def action_debug_task(modeladmin, request, queryset):
    debug_task.delay()


@admin.action(description="Consultar DTE")
def action_consultar_dte(modeladmin, request, queryset):
    clientes = list(queryset.values_list("id", flat=True))
    task_consultar_dte.delay(clientes)
