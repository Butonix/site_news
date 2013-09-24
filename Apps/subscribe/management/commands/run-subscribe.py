from django.core.management.base import BaseCommand
from subscribe.models import Member, Subscribe
from django.template import Context, loader
from datetime import datetime
from django.core.mail import EmailMessage


SUBJ = u'Рассылка новостей сайта mk.mk.ua'
FROM = 'subscribe@mk.mk.ua'

class Command(BaseCommand):
    def handle(self, *args, **options):
        members = Member.objects.filter(is_active=1)
        subscribes = Subscribe.objects.filter(date__lte=datetime.now())                        
        
        for subscribe in subscribes:
            t = loader.get_template('emails/news.html')
            c = {'subscribe': subscribe}
            
            for member in members:
                msg = EmailMessage(SUBJ, t.render(Context(c)), FROM, [member.email])
                msg.content_subtype = "html"
                msg.send()
            
            subscribe.delete()
        
            