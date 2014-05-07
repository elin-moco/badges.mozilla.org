from django.core.management.base import BaseCommand
from badgus.mocotw.utils import moztech_award_ceremony


class Command(BaseCommand):
    args = ''
    help = 'Update awards from MozTech'

    def handle(self, *args, **options):
        moztech_award_ceremony()
