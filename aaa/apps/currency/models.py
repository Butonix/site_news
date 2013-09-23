from django.db import models
from django.contrib import admin

# модель банков

class Company(models.Model):
    name = models.CharField(u'Банк', max_length=100, blank=True)
    logo = models.ImageField(u'Логотип', upload_to='logos/', blank=True)
    title = models.CharField(u'Имя для админки', max_length=100)
    
    def __unicode__(self):
        if self.name:
            return self.name
        return self.title
        
    class Meta:
        verbose_name = u'банк'
        verbose_name_plural = u'банки'
     
# День, за который представлены курсы валют
     
class Date(models.Model):    
    date = models.DateField(u'Дата')
    
    def __unicode__(self):
        return u'курсы валют за %s' % self.date.strftime('%d.%m.%Y')
    
    class Meta:
        verbose_name = u'курсы'
        verbose_name_plural = u'курсы валют'

# курсы обмена        
        
class Exchange(models.Model):
    company = models.ForeignKey(Company, verbose_name=u'Банк')
    date = models.ForeignKey(Date, related_name='exchange')
    eur_buy = models.FloatField(u'Покупка EUR')
    eur_sell = models.FloatField(u'Продажа EUR')
    usd_buy = models.FloatField(u'Покупка USD')    
    usd_sell = models.FloatField(u'Продажа USD')    
    rur_buy = models.FloatField(u'Покупка RUR')
    rur_sell = models.FloatField(u'Продажа RUR')
        

class ExchangeInline(admin.TabularInline):
    model = Exchange
    extra = 5
        
class DateAdmin(admin.ModelAdmin):
    inlines = [ExchangeInline]

class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Date, DateAdmin)
admin.site.register(Company, CompanyAdmin)    
