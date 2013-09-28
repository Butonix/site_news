from django.db import models
#from django.contrib import admin
from Compat.tagging.fields import TagField
from Compat.thumbnail.fields import ThumbField


class Report(models.Model):    
    pub_date = models.DateTimeField(u'Дата публикации', null=True, blank=True)
    title = models.CharField(u'Заголовок', max_length=255)
    text = models.TextField(u'Описание репортажа')
    photo = models.ImageField('Основное фото', upload_to='photos/report/%Y/%m/%d', blank=False)
    thumb_big = ThumbField(source='photo', size=[197,132], upload_to='photos/report/%Y/%m/%d', )
    thumb_small = ThumbField(source='photo', size=[72,65], upload_to='photos/report/%Y/%m/%d', )
    view_count = models.PositiveIntegerField('Просмотров', default=0)
    comment_count = models.PositiveIntegerField('Комментариев', default=0)
    tags = TagField('Теги реп ортажа', blank=True)
    published = models.BooleanField(u'Опубликован', default=0)
    
    def get_pub_date(self):
        if self.published:
            return self.pub_date.strftime('%d.%m.%Y %H:%M')
        return 'Не опубликован'

    get_pub_date.short_description = 'Дата публикации'
    
    # Пересчет комментариев
    
    def update_comment_count(self):
        self.comment_count = self.comments.count()
        self.save()

    # Увеличение количества просмотров
        
    def increase_view(self):
        self.view_count = self.view_count + 1
        self.save()
    
    # Абсолютный адрес репортажа
    
    def get_absolute_url(self):
        return u'/photoreport/%d/%.2d/%.2d/%.5d/' % (self.pub_date.year, 
            self.pub_date.month, self.pub_date.day, self.pk)
    
    def __unicode__(self):
        if self.published:
            return '[%.2d.%.2d.%.4d] %s' % (self.pub_date.day, 
                self.pub_date.month, self.pub_date.year, 
                self.title)
        else:
            return self.title
    
    class Meta:
        verbose_name = u'фоторепортаж'
        verbose_name_plural = u'фоторепортажи'

# Модель комментарив пользователей        

class Comment(models.Model):
    report = models.ForeignKey(Report, related_name='comments', verbose_name='Новость')
    email = models.EmailField(u'Email', blank=True)
    user_name = models.CharField(u'Имя', max_length=100)
    pub_date = models.DateTimeField(u'Дата добавления', auto_now_add=True)
    text = models.TextField('Текст')
    
    def __unicode__(self):
        return self.email
        
    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        ordering = ["-pub_date"]

    # вызов пересчет комментариев новости при добавлении
    
    def save(self):
        if self.id:
            old = Comment.objects.get(pk=self.id)
            super(Comment, self).save()
            self.report.update_comment_count()
            if self.report != old.report:
                old.report.update_comment_count()        
        else:
            super(Comment, self).save()
            self.report.update_comment_count()            

    # вызов пересчет комментариев новости при удалении

    def delete(self):   
        super(Comment, self).delete()
        self.report.update_comment_count()
        

class Photo(models.Model):
    report = models.ForeignKey(Report, related_name='photos')
    text = models.TextField(u'Описание фотографии', blank=True)
    photo = models.ImageField('Фото', upload_to='photos/report/%Y/%m/%d', blank=False)
    thumb_big = ThumbField(source='photo', size=[197,132], upload_to='photos/report/%Y/%m/%d', )

#admin.site.register(Photo, PhotoAdmin)