from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from news.models import News
        news = News.objects.all() #filter(add_date__gte=date_filter, )
        for each_news in news:
            print each_news.pk
            each_news.update_comment_count()
#            obj = Counters.objects.get(news=each_news, )
#            obj.commets=each_news.comment_count
#            obj.save()
#    return HttpResponseRedirect('/')