from django.core.management.base import BaseCommand
from pedidos.services import TinyService

class Command(BaseCommand):
	help = "Sincroniza pedidos do Tiny para o banco de Dados Local."

	def handle(self, *args, **options):
		tiny = TinyService()
		result = tiny.fetch_pedidos()
		self.stdout.write(self.style.SUCCESS(f"importados {result.get('imported', 0)} pedidos do Tiny."))

		