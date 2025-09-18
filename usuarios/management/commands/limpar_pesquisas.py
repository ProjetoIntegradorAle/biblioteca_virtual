from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from app.models import HistoricoPesquisa

class Command(BaseCommand):
    help = 'Remove pesquisas com mais de 30 dias'

    def handle(self, *args, **kwargs):
        limite = timezone.now() - timedelta(days=30)
        deletados = HistoricoPesquisa.objects.filter(data_pesquisa__lt=limite).delete()
        self.stdout.write(f"{deletados[0]} pesquisas antigas removidas.")
