from django.core.management.base import BaseCommand
from playbill.models import Event
from datetime import date


SUBJ = u'Рассылка новостей сайта mk.mk.ua'
FROM = 'subscribe@mk.mk.ua'

class Command(BaseCommand):
    def handle(self, *args, **options):
        old = Event.objects.filter(end_date__lt=date.today())
        for event in old:
            event.delete()
            
            