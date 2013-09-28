# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from Compat.thumbnail.fields import ThumbField
from Apps.news.managers import Manager
from Compat.tagging.fields import TagField


# Модель рубрики
class Rubric(models.Model):
    name = models.CharField(u'Рубрика', max_length=255)
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(u'Slug')
    keywords = models.CharField(u'Ключевые слова', max_length=255, blank=True)
    description = models.TextField(u'Описание', blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/rubric/%s/' % self.slug

    class Meta:
        verbose_name = "рубрика"
        verbose_name_plural = "рубрики"


# Модель новости
class News(models.Model):

    # Основные свойства новости
    title = models.CharField(u'Заголовок', max_length=255)
    author = models.ForeignKey(User, related_name='news', verbose_name='Автор')
    rubric = models.ForeignKey(Rubric, related_name='news', verbose_name='Рубрика')

    # Текстовые новости
    text_middle = models.TextField(u'Короткий текст', help_text='Текст для вывода на главной в рубриках')
    text_big = models.TextField(u'Полный текст')
    LANG_CHOICES = (
        (1, 'Russian'),
        (2, 'Ukraine'),
    )
    lang = models.PositiveSmallIntegerField(choices=LANG_CHOICES, default=1, )
    text_first_locked = models.TextField(u'Текст для главной страницы', help_text='если стоит "закреплена на главной"', blank=True)
    external_author = models.CharField(u'Внешний источник', max_length=255, blank=True)

    # Картинки
    # Абсолютный путь к дополнительной фотографии
    def set_path_photo(self, filename, ):
        if self.pub_date:
            return 'photos/news/%s/%s' % (self.pub_date.strftime('%Y/%m/%d'), filename, )
        else:
            from datetime import datetime
            return 'photos/news/%s/%s' % (datetime.now().strftime('%Y/%m/%d'), filename, )
    #photo = models.ImageField('Фото', upload_to=set_path_photo, blank=False, null=False, )
    #thumb_main = ThumbField(source='photo', img_size=[298,198], upload_to=set_path_photo)
    #thumb_big = ThumbField(source='photo', img_size=[197,132], upload_to=set_path_photo, )
    #thumb_middle = ThumbField(source='photo', img_size=[88,65], upload_to=set_path_photo, )
    #thumb_small = ThumbField(source='photo', img_size=[38,38], upload_to=set_path_photo, )

    photo = models.ImageField('Фото', upload_to=set_path_photo, blank=False, null=False, )
    thumb_main = ThumbField(source='photo', size=[298,198], upload_to=set_path_photo, )
    #  upload_to='photos/news/%Y/%m/%d', )
    thumb_big = ThumbField(source='photo', size=[197,132], upload_to=set_path_photo, )
    thumb_middle = ThumbField(source='photo', size=[88,65], upload_to=set_path_photo, )
    thumb_small = ThumbField(source='photo', size=[38,38], upload_to=set_path_photo, )

    # Дополнительные свойства
    photo_sign = models.CharField(u'Подпись к фото', max_length=255, blank=True)
    first_locked = models.BooleanField(u'На главной', default=0, help_text='Новость будет закреплена на главной')
    rubric_locked = models.BooleanField(u'В рубрике', default=0, help_text='Новость будет закреплена в рубрике')
    published = models.BooleanField(u'Опубликована', default=0)
#    changed = models.BooleanField(verbose_name=u'Флаг изменений', default=False, )
    add_date = models.DateTimeField(u'Дата добавления', auto_now_add=True)
    show_in_newslist = models.BooleanField(u'В ленте', default=1,
                                           help_text='Новость будет отображаться в ленте новостей')
    bold_title = models.BooleanField(u'Выделять заголовок', default=0, help_text='Новость будет выделена жирным')
    pub_date = models.DateTimeField(u'Дата публикации', null=True, blank=True)
    tags = TagField('Теги новости', blank=True)
    keywords = models.CharField(u'Клчевые слова', max_length=255, blank=True)

    # Просмотр и комментарии
#    view_count = models.PositiveIntegerField('Просмотров', blank=False, null=False, default=0, ) #default=0
#    comment_count = models.PositiveIntegerField('Комментариев', blank=False, null=False, default=0, ) #default=0

    # Менеджеры
    objects = Manager()

    def views_count(self):
        from django.core.cache import cache
        # try to get product from cache
        counters = cache.get(u'counters_%d' % self.pk, )
        # if a cache miss, fall back on db query
        if not counters:
            try:
                counters = Counters.objects.get(news=self, )
            except Counters.DoesNotExist:
                Counters.objects.create(news=self, )
                return 0
            # store item in cache for next time
            else:
                cache.set(u'counters_%d' % self.pk, counters, 300, )
                return counters.viewers
        else:
            return counters.viewers

#        from django.shortcuts import get_object_or_404
#        try:
#            views = Counters.objects.get(news=self, ).viewers
#        except Counters.DoesNotExist:
#            Counter.objects.create(news=self, )
#            return 0
#        else:
#            return views
##        return get_object_or_404(Views, news=self.pk).views_count

    def comment_count(self):
        from django.core.cache import cache
        # try to get product from cache
        counters = cache.get(u'counters_%d' % self.pk, )
        # if a cache miss, fall back on db query
        if not counters:
            try:
                counters = Counters.objects.get(news=self, )
            except Counters.DoesNotExist:
                Counters.objects.create(news=self, )
                return 0
            # store item in cache for next time
            else:
                cache.set(u'counters_%d' % self.pk, counters, 300, )
                return counters.comments
        else:
            return counters.comments
##        from django.shortcuts import get_object_or_404
#        try:
#            comments = Counters.objects.get(news=self, ).comments
#        except Counters.DoesNotExist:
#            Counter.objects.create(news=self, )
#            return 0
#        else:
#            return comments
##        return get_object_or_404(Views, news=self.pk).views_count

    def increase_view(self):
#        self.view_count = self.view_count + 1
#        self.save()
        try:
            views = Counters.objects.get(news=self, )
        except Counters.DoesNotExist:
            views = Counters.objects.create(news=self, viewers=1, )
            return 1
        else:
            from django.db.models import F
            views.viewers = F('viewers') + 1
            views.save() #update_fields=['views_count']
            return Counters.objects.get(news=self, ).viewers

    def save(self, *args, **kwargs):
#        import Image as pil
#        name=self.photo.name
#        path=self.photo.path
#        photo=self.photo
#        self_photo=self
#        import os
##        self.thumb_main.save(os.path.basename(self.photo.path), self.photo, save=False, )
##        img = pil.open(self.thumb_main.path, )
#        img = pil.open(self.photo, )
#        raw = self.rescale(img, self.thumb_main.img_size[0], self.thumb_main.img_size[1], )
##        photo_path = 'photos/news/%s' % self.pub_date.strftime('%Y/%m/%d')
##        import os
##        self.thumb_main.name = os.path.join(photo_path, self.generate_thumb_name(self.photo.path, 'thumb_main', ), )
##        thumb_main = getattr(self, 'thumb_main', None, )
##        thumb_main.save(self.thumb_main.name, content=ContentFile(raw), save=False, )
##        if self.changed:
##            from datetime import datetime
##            now = datetime.now()
##            date_string = now.strftime('%Y/%m/%d')
##            photo_path = 'photos/news/%s' % date_string
##            import os
##            self.thumb_main.name = os.path.join(photo_path, self.generate_thumb_name(self.photo.path, 'thumb_main', ), )
##            self.thumb_big.name = os.path.join(photo_path, self.generate_thumb_name(self.photo.path, 'thumb_big', ), )
##            self.thumb_middle.name = os.path.join(photo_path, self.generate_thumb_name(self.photo.path, 'thumb_middle', ), )
##            self.thumb_small.name = os.path.join(photo_path, self.generate_thumb_name(self.photo.path, 'thumb_small', ), )
##        raw_thumb_main = rescale(self.photo.path, self.size[0], self.size[1], )
##        raw_thumb_big = rescale(self.photo.path, self.size[0], self.size[1], )
##        raw_thumb_middle = rescale(self.photo.path, self.size[0], self.size[1], )
##        raw_thumb_small = rescale(self.photo.path, self.size[0], self.size[1], )
        super(News, self).save(*args, **kwargs)
   #     SEARCH_ENGINE_PING_URLS = (
   #         ('http://www.google.com/webmasters/tools/ping'),
   #         ('http://webmaster.yandex.ru/wmconsole/sitemap_list.xml'),
   #         ('http://search.yahooapis.com/SiteExplorerService/V1/ping'),
   #         ('http://submissions.ask.com/ping'),
   #         ('http://webmaster.live.com/ping.aspx'),
   #     )
#        SEARCH_ENGINE_PING_URLS = (
#            ('google', 'http://www.google.com/webmasters/tools/ping'),
#            ('yahoo', 'http://search.yahooapis.com/SiteExplorerService/V1/ping'),
#            ('ask', 'http://submissions.ask.com/ping'),
#            ('live', 'http://webmaster.live.com/ping.aspx'),
#        )
#        successfully_pinged = []
        # We do this once now, so ping_google
        # doesn't do it for every iteration.
   #     from django.core.urlresolvers import reverse
   #     sitemap_url = reverse('static_sitemaps_index')
#        for (site, url) in SEARCH_ENGINE_PING_URLS:
   #     from django.contrib.sitemaps import ping_google
   #     for url in SEARCH_ENGINE_PING_URLS:
   #         try:
   #             ping_google(sitemap_url=sitemap_url, ping_url=url)
#                pinged = True
   #         except:
   #             pass
#                pinged = False
#            if pinged:
#                successfully_pinged.append(site)
#        return successfully_pinged

        try:
            Counters.objects.get(news=self, )
        except Counters.DoesNotExist:
            Counters.objects.create(news=self, )

    # Отрисовка в админке - или дата публикации или тект
    def get_pub_date(self):
        if self.published:
            return self.pub_date.strftime('%d.%m.%Y %H:%M')
        return 'Не опубликована'

    get_pub_date.short_description = 'Дата публикации'

    # Пересчет комментариев
    def update_comment_count(self):
        try:
            counters = Counters.objects.get(news=self, )
        except Counters.DoesNotExist:
            Counters.objects.create(news=self, comments=self.model_comments.count(), )
        else:
            counters.comments = self.model_comments.count()
            counters.save() #update_fields=['views_count']
#        self.counters.comments = self.comments.count()
#        self.save()

    # Абсолютный адрес новости
    def get_absolute_url(self):
        if self.pub_date:
            return '/rubric/%s/%d/%.2d/%.2d/%.5d/' % (self.rubric.slug,
                                                      self.pub_date.year,
                                                      self.pub_date.month,
                                                      self.pub_date.day,
                                                      self.pk)
        else:
            return '/rubric/not_published/'

    def __unicode__(self):
#        if self.pub_date:
#            return '%s [%s] - Mk.Mk.ua' % (self.title, self.pub_date.strftime(u'%d.%m.%Y', ), )
##            return '[%.2d.%.2d.%.4d] %s' % (self.pub_date.day, 
##                self.pub_date.month, self.pub_date.year, 
##                self.title)
#        else:
            return self.title

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"

#class Changed(models.Model):
#    news = models.ForeignKey(News, verbose_name='Новость', related_name='changed', blank=False, null=False, )
#    changed_thumb_main = models.BooleanField(verbose_name=u'Флаг изменений thumb_main', default=False, )
#    changed_thumb_big = models.BooleanField(verbose_name=u'Флаг изменений thumb_big', default=False, )
#    changed_thumb_middle = models.BooleanField(verbose_name=u'Флаг изменений thumb_middle', default=False, )
#    changed_thumb_small = models.BooleanField(verbose_name=u'Флаг изменений thumb_small', default=False, )

#    class Meta:
#        db_table = 'Changed'
#        verbose_name = u'флаг изменения'
#        verbose_name_plural = u'флаги изменений'


class Counters(models.Model):
    news = models.ForeignKey(News,
                             verbose_name='Новость',
                             related_name='model_counters',
                             blank=False,
                             null=False, )
    viewers = models.PositiveSmallIntegerField(verbose_name=u'Количество просмотров',
                                               blank=True,
                                               null=True,
                                               default=0, )
    comments = models.PositiveSmallIntegerField(verbose_name=u'Количество комментариев',
                                                blank=True,
                                                null=True,
                                                default=0, )

    # Менеджеры
    objects = Manager()

#    # Увеличение количества просмотров
#    def increase_view(self):
#        self.count = self.count + 1
#        self.save()

    class Meta:
        db_table = 'Counters'
        verbose_name = u'количество просмотров'
        verbose_name_plural = u'количество просмотров'


# Модель доподнительных фотографий для новости
class Photo(models.Model):
    news = models.ForeignKey(News, related_name='photos', verbose_name='Новость')
    sign = models.CharField(u'Подпись', max_length=255)

    def set_path_photo(self, filename, ):
        if self.news.pub_date:
            return 'photos/extra/%s/%s' % ( self.news.pub_date.strftime('%Y/%m/%d'), filename, )
        else:
#            from datetime import datetime
            return 'photos/extra/%s/%s' % (self.news.add_date.strftime('%Y/%m/%d'), filename, )  # datetime.now()
    image = models.ImageField(u'Фото', upload_to=set_path_photo, blank=False, null=False, )  # 'photos/extra/%Y/%m/%d'
    thumb = ThumbField(source='image', size=[88, 65, ], upload_to=set_path_photo, )

#    def generate_thumb_name(self, original, field_name, ):
#        import os
#        filename = os.path.split(original)[-1].split('.')
#        if len(filename) > 1:
#            filename[-2] = filename[-2] + '.' + field_name
#        else:
#            filename.append('.'+self._field_name)
#        return '.'.join(filename)
#
#    def save(self, *args, **kwargs):
#        from datetime import datetime
#        now = datetime.now()
#        date_string = now.strftime('%Y/%m/%d')
#        photo_path = 'photos/extra/%s' % date_string
#        import os
#        self.thumb.name = os.path.join(photo_path, self.generate_thumb_name(self.photo.path, 'thumb', ), )
#        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'фотографии'
        verbose_name_plural = u'дополнительные фотографии'


# Модель комментарив пользователей
class Comment(models.Model):
    news = models.ForeignKey(News, related_name='model_comments', verbose_name='Новость', )
    email = models.EmailField(u'Email', blank=True, )
    user_name = models.CharField(u'Имя', max_length=100, )
    pub_date = models.DateTimeField(u'Дата добавления', auto_now_add=True, )
    text = models.TextField('Текст', )

    def __unicode__(self):
        return self.email

    def news_link(self):
        return '<a href="%s">%s</a>' % (self.news.get_absolute_url(), self.news.title, )
    news_link.allow_tags = True

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        ordering = ["-pub_date"]

    # вызов пересчет комментариев новости при добавлении
    def save(self):
        if self.id:
            old = Comment.objects.get(pk=self.id)
            super(Comment, self).save()
            self.news.update_comment_count()
            if self.news != old.news:
                old.news.update_comment_count()
        else:
            super(Comment, self).save()
            self.news.update_comment_count()

    # вызов пересчет комментариев новости при удалении
    def delete(self):
        super(Comment, self).delete()
        self.news.update_comment_count()
