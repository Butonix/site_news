from django.db import models
from django.contrib import admin
from thumbnail.fields import ThumbField

class Type(models.Model):
    name = models.CharField(u'Тип', max_length=100)
    add_date = models.DateTimeField(u'Дата добавления', auto_now=True)
        
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = u'тип событий'
        verbose_name_plural = u'типы событий'

class Place(models.Model):
    name = models.CharField(u'Место', max_length=100)
    info = models.CharField(u'Информация', max_length=255)
    logo = models.ImageField(u'Лого', upload_to='playbill/', blank=True)
    type = models.ForeignKey(Type, verbose_name=u'Тип событий')
    add_date = models.DateTimeField(u'Дата добавления', auto_now=True)    
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = u'место события'
        verbose_name_plural = u'места событий'
        
class Event(models.Model):
    place = models.ForeignKey(Place, verbose_name='место события')
    start_date = models.DateField(u'Дата начала')
    end_date = models.DateField(u'Дата окончания')
    text = models.TextField(u'Описание')
    allow_future = models.BooleanField(u'Показывать в "Скоро"', default=0)
    add_date = models.DateTimeField(u'Дата добавления', auto_now=True)
    photo = models.ImageField('Фото', upload_to='playbill/events', blank=True)
    thumb = ThumbField(source='photo', size=[60,60], upload_to='playbill/events', )
    
    def get_place_type(self):
        return self.place.type
    
    def __unicode__(self):
        return u'[%s-%s] %s' % (self.start_date, self.end_date, self.place)

    class Meta:
        verbose_name = u'событие'
        verbose_name_plural = u'события'
    
    
class EventAdmin(admin.ModelAdmin):
    list_display = ['start_date','end_date','get_place_type','place','text']
    exclude = ['thumb']
    ordering = ['-start_date']

class PlaceAdmin(admin.ModelAdmin):
    ordering = ['-add_date']

class TypeAdmin(admin.ModelAdmin):
    ordering = ['-add_date']
    
admin.site.register(Type, TypeAdmin)
admin.site.register(Place, PlaceAdmin)    
admin.site.register(Event, EventAdmin)