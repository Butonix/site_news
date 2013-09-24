from django.contrib import admin
from Apps.news.models import Rubric, News, Counters, Photo, Comment
#import datetime

class PhotoAdmin(admin.TabularInline):
    exclude = ['thumb']
    model = Photo
    extra = 5

class NewsAdmin(admin.ModelAdmin):
#    exclude = ['add_date', 'view_count', 'published', 'comment_count', 'thumb_big', 'thumb_middle', 'thumb_small', 'thumb_main']
    exclude = ['published', 'thumb_main', 'thumb_big', 'thumb_middle', 'thumb_small', ] # 'view_count',  'comment_count',
    list_display = ['get_pub_date', 'title', 'rubric', 'author', 'first_locked', 'rubric_locked', 'show_in_newslist','add_date', 'tags', ]  # 'comment_count',
    search_fields = ['title', 'text_first_locked', 'text_middle', 'text_big', ]
    list_display_links = ['title', ]
    ordering = ['-pub_date', ]

    # Дополнительные поля
    list_filter_user = ['rubric', ]
    list_filter_admin = ['published', 'rubric', 'pub_date', 'first_locked', 'rubric_locked', 'author', ]
    hide_to_user = ['author', 'first_locked', 'rubric_locked', 'tags', 'pub_date', ]

    # Выбираем для авторов только их новости

    inlines = [PhotoAdmin]

    def queryset(self, request, ):
        qs = super(NewsAdmin, self).queryset(request, )
        if not request.user.is_superuser:
            qs = qs.filter(author=request.user, published=0, )
        return qs

    # Убираем для авторов hide_to_user поля

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(NewsAdmin, self).get_fieldsets(request, obj)
        for set in fieldsets:
            if not request.user.is_superuser:
                set[1]['fields'] = [x for x in set[1]['fields']
                    if x not in self.hide_to_user]
        return fieldsets

    # Настраиваем фильтры

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter = self.list_filter_admin
        else: 
            self.list_filter = self.list_filter_user
        parent = super(NewsAdmin, self)
        return parent.changelist_view(request, extra_context)

    # Выставляем флаг published если есть pub_date
    # Если были выствлены флаги first_locked и rubric_locked,
    # с остальных новостей они снимаются

    def save_model(self, request, obj, form, change, ):
        obj.published = obj.pub_date is not None
        if obj.first_locked:
            News.objects.update(first_locked=0, )
        if obj.rubric_locked:
            qs = News.objects.filter(rubric=obj.rubric, )
            qs.update(rubric_locked=0, )

#        try:
#           obj_get = News.objects.get(pk=obj.pk, )
#        except News.DoesNotExist:
#            pass
#        else:
##            url_with_file_output = u'/usr/local/www/mk_mk_mk_ua/media/photos/test-file.txt'
##            file_output = open(url_with_file_output, mode='wb+', buffering=False, )
#            obj_get_photo_path_split = obj_get.photo.path.split('/')[-1]
#            obj_get_photo_path_split = obj_get_photo_path_split.split('.')
#            string = ''
#            for n in range(0, len(obj_get_photo_path_split) - 1):
#                string = string.join(obj_get_photo_path_split[n])
#            string = string.split('_')
#            str = ''
#            if string[-1].isdigit():
#                integer = int(string[-1])
#                if integer > 0 and integer < 11:
#                    for n in range(0, len(string) - 1):
#                        str = str.join(string[n])
##            str = '%s'str.join(obj_get_photo_path_split[-1])
#            if str == '':
#                for n in range(0, len(string)):
#                    str = str.join(string[n])
#            str = '%s.%s' % (str, obj_get_photo_path_split[-1], )
#            obj_photo_path_split = obj.photo.path.split('/')[-1]
#            if str != obj_photo_path_split:
#                try:
#                    changed = Changed.objects.get(pk=obj.pk, )
#                except Changed.DoesNotExist:
#                    Changed.objects.create(pk=obj.pk, news=obj, changed_thumb_main = True, changed_thumb_big = True, changed_thumb_middle = True, changed_thumb_small = True, )
#                else:
#                    changed.changed_thumb_main = True
#                    changed.changed_thumb_big = True
#                    changed.changed_thumb_middle = True
#                    changed.changed_thumb_small = True
#                    changed.save()
##            if obj_get.photo.path != obj.photo.path
##            file_output.write(u'obj_get.photo.path - ' + obj_get.photo.path + u'\n' + str + '\n') #obj_get_photo_path_split + '\n' + 
##            file_output.write(u'obj.photo.path - ' + obj.photo.path + u'\n' + obj_photo_path_split + '\n')
##            file_output.close()

##        if change:
##            obj.changed = True

        obj.save()

    # Если новость добавляет автор, подставляем его id
    def change_view(self, request, obj_id):
        if request.method == 'POST' and not request.user.is_superuser:
            request.POST['author'] = request.user.id
        return super(NewsAdmin, self).change_view(request, obj_id)

    def add_view(self, request):
        if request.method == 'POST' and not request.user.is_superuser:
            request.POST['author'] = request.user.id
        return super(NewsAdmin, self).add_view(request)


class RubricAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    ordering = ['-date']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['pub_date', 'email', 'news_link', 'text']
    search_fields = ['text', 'email']
    list_filter = ['pub_date']
    ordering = ['-pub_date']


admin.site.register(Comment, CommentAdmin, )
admin.site.register(News, NewsAdmin, )
#admin.site.register(Changed, )
admin.site.register(Counters, )
admin.site.register(Rubric, RubricAdmin, )
