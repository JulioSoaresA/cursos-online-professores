from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Adiciona os cursos'

    def handle(self, *args, **options):
        call_command('loaddata', 'eixos_tematicos.json')
