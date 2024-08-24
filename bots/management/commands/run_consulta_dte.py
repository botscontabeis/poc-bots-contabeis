from django.core.management.base import BaseCommand

from bots.tasks.uvt import task_consultar_dte
from core.models import Cliente


class Command(BaseCommand):
    help = "Executa o bot de Consulta DTE para TODOS os clientes cadastrados."

    def handle(self, *args, **options):
        self.stdout.write("Iniciando consulta DTE para todos os clientes")

        self.stdout.write("Buscando clientes")
        clientes = list(Cliente.objects.values_list("id", flat=True))

        self.stdout.write("Disparando task_consultar_dte")
        task_consultar_dte.delay(clientes)
