from django.core.management.base import BaseCommand
from badgus.mocotw.utils import export_authors


class Command(BaseCommand):
    args = ''
    help = 'Update awards from MozTech'

    def handle(self, *args, **options):
        export_authors()

