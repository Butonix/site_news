from django.db import models
from news.models import News
from django.contrib import admin
import sha, os, datetime

KEY_EXPIRE = 3

class Member(models.Model):
    email = models.EmailField(u'Email', unique=True)
    is_active = models.BooleanField(u'Активный', default=0)
    
    def __unicode__(self):
        return self.email
        
    class Meta:
        verbose_name = u'подписчик'
        verbose_name_plural = u'подписчики'

class Subscribe(models.Model):
    date = models.DateTimeField('Дата рассылки')

    class Meta:
        verbose_name = u'рассылка'
        verbose_name_plural = u'рассылки'        
        
    def __unicode__(self):
        return u'Рассылка новостей. Запланирована на %s' % (self.date.strftime('%d.%m.%Y %H:%M'))
        
class Selected(models.Model):
    news = models.OneToOneField(News, verbose_name='Новость')
    subscribe = models.ForeignKey(Subscribe, verbose_name='Рассылка', related_name='selected')
    
    class Meta:
        verbose_name = u'новость рассылки'
        verbose_name_plural = u'новости'

    def __unicode__(self):
        return u'%s' % self.news
     
class Activation(models.Model):
    user = models.ForeignKey(Member, unique=True)
    key = models.CharField(max_length=255, primary_key=True)
    action = models.BooleanField(default=0) # 0 - отписаться, 1-подписаться
    expires = models.DateTimeField()
	
    def save(self):
        self.key = sha.new(os.urandom(20)).hexdigest()
        self.expires = datetime.datetime.today() + datetime.timedelta(KEY_EXPIRE)
        super(Activation, self).save()        
        
class SelectedInline(admin.TabularInline):
    model = Selected
    extra = 10        
    
class MemberAdmin(admin.ModelAdmin):
    pass

class SubscribeAdmin(admin.ModelAdmin):
    inlines = [SelectedInline]    

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        for form in context['inline_admin_formsets'][0].formset.forms:
            form.fields['news'].queryset = News.objects.newslist(20)
        return super(SubscribeAdmin, self).render_change_form(request,
            context, add, change, form_url, obj) 

    
admin.site.register(Member, MemberAdmin)
admin.site.register(Subscribe, SubscribeAdmin)    
