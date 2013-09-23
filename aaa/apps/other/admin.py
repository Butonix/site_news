__author__ = 'Sergey'

from django.contrib import admin
from models import Banner, Announce


class BannerAdmin(admin.ModelAdmin):
    ordering = ['-date']


class AnnounceAdmin(admin.ModelAdmin):
    ordering = ['-date']


admin.site.register(Banner, BannerAdmin)
admin.site.register(Announce, AnnounceAdmin)

