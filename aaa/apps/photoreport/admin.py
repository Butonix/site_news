__author__ = 'Sergey'

from django.contrib import admin
from models import Report, Photo


class PhotoAdmin(admin.StackedInline):
    exclude = ['thumb_big']
    model = Photo
    extra = 20


class ReportAdmin(admin.ModelAdmin):
    exclude = ['view_count', 'published', 'comment_count', 'thumb_big', 'thumb_small',]
    list_display = ['get_pub_date', 'title', 'comment_count', 'tags']
    list_display_links = ['title']
    ordering = ['-pub_date']
    inlines = [PhotoAdmin]

    def save_model(self, request, obj, form, change):
        obj.published = obj.pub_date is not None
        obj.save()

admin.site.register(Report, ReportAdmin)

