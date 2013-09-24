# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
#from models import News, Views

class Manager(models.Manager):

    # Все опубликованные новости

    def published(self):
#        self = self.select_related() # .select_related(depth=2)
        return self.filter(published=1).order_by('-pub_date')

    # Закрепленная на главной.
    # Всегда нужно проверять на None
    def first_locked(self):
        from django.core.cache import cache
        # try to get product from cache
        first_locked = cache.get(u'first_locked', )
        # if a cache miss, fall back on db query
        if not first_locked:
            try:
                first_locked = self.published().get(first_locked=1, )
            except self.model.DoesNotExist:
                return None
            # store item in cache for next time
            else:
                cache.set(u'first_locked', first_locked, 900, ) # 1h
                return first_locked
        else:
            return first_locked
#    from django.core.cache import cache
#    # try to get product from cache
#    banner_top = cache.get(u'baner_top', )
#    # if a cache miss, fall back on db query
#    if not banner_top:
#        try:
#            banner_top = Banner.objects.filter(place=1).order_by('-date')[0]
#        except Banner.DoesNotExist:
#            banner_top = None
#        # store item in cache for next time
#        else:
#            cache.set(u'baner_top', banner_top, 3600, ) # 1h

    # Закрепленные в рубриках
    def rubric_locked(self, rubric=None):
        qs = self.published()
        if rubric:
            try:
                return qs.get(rubric_locked=1, rubric=rubric)
            except self.model.DoesNotExist:
                return None
        else:
            qs = qs.filter(rubric_locked=1, first_locked=0)
            return qs

    # Новости без флагов "закреплено"
    def with_no_flags(self, limit=5):
        qs = self.published()
        return qs.filter(first_locked=0, rubric_locked=0)[:limit]

    # Популярные
#    def popular_view2(self, limit=3):
#        from datetime import datetime, timedelta
#        qs = self.published().filter(pub_date__gte=(datetime.now() - timedelta(7)))
#        return qs.order_by('-view_count')[:limit]

    def popular_view(self, limit=3):
        from datetime import datetime, timedelta
        qs = self.published().filter(pub_date__gte=(datetime.now() - timedelta(14)))
        return qs.order_by('-model_counters__viewers')[:limit]

    def popular_comment(self, limit=3):
        from datetime import datetime, timedelta
        qs = self.published().filter(pub_date__gte=(datetime.now() - timedelta(14)))
        return qs.order_by('-model_counters__comments')[:limit]

    def newslist(self, limit=20):
        return self.published()[:limit]
#        return self.published().filter(show_in_newslist=1)[:limit]
