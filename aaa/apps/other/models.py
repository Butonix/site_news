# coding=utf-8
from django.db import models
#from django.contrib import admin

# Баннеры

CHOICES = [(1, u'вверху'), (2, u'правая колонка')]


class Banner(models.Model):
    place = models.IntegerField(u'Расположение', choices=CHOICES)
    date = models.DateTimeField(u'Дата', auto_now=True)
    link = models.URLField(u'Ссылка', blank=True)
    image = models.ImageField(u'Картинка', upload_to='banners/', blank=True)    
    code = models.TextField(u'Код баненера', blank=True)
    
    def __unicode__(self):
        for k,v in CHOICES:
            if k == self.place:
                if self.code: return u'баннер [%s], код. Изменен %s' % (v, self.date.strftime('%d.%m.%Y %H:%M'))
                else: return u'баннер [%s], картинка. Изменен %s' % (v, self.date.strftime('%d.%m.%Y %H:%M'))
        
    class Meta:
        verbose_name = u'баннер'
        verbose_name_plural = u'баннеры'


# Анонсы
class Announce(models.Model):
    date = models.DateTimeField(u'Дата', auto_now=True)
    title = models.CharField(u'Заголовок', max_length=255)
    image = models.ImageField(u'Картинка', upload_to='banners/', blank=True)
    link = models.URLField(u'Ссылка', blank=True)
    text = models.TextField(u'Текст')
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = u'анонс'
        verbose_name_plural = u'анонсы'
