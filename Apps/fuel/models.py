from django.db import models
from django.contrib import admin

class Company(models.Model):
    company = models.CharField(u'Компания', max_length=100)
    logo = models.ImageField(u'Логотип', upload_to='logos/', blank=True)
    
    def __unicode__(self):
        return self.company
        
    class Meta:
        verbose_name = u'компания'
        verbose_name_plural = u'компании'
     
        
class Date(models.Model):    
    date = models.DateField(u'Дата')
    
    def __unicode__(self):
        return u'Цены на топливо за %s' % self.date.strftime('%d.%m.%Y')
    
    class Meta:
        verbose_name = u'цены'
        verbose_name_plural = u'цены на топливо'

class Price(models.Model):
    company = models.ForeignKey(Company, verbose_name=u'Компания')
    date = models.ForeignKey(Date, related_name='price')
    a98 = models.FloatField(u'A98')
    a95 = models.FloatField(u'A95')
    a92 = models.FloatField(u'A92')
    a76 = models.FloatField(u'A76')
    dt = models.FloatField(u'ДТ')
        
class PriceInline(admin.TabularInline):
    model = Price
    extra = 5
        
class DateAdmin(admin.ModelAdmin):
    inlines = [PriceInline]

class CompanyAdmin(admin.ModelAdmin):
    pass    

admin.site.register(Date, DateAdmin)
admin.site.register(Company, CompanyAdmin)    
