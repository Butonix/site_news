from django.contrib import admin
from Compat.tagging.models import Tag, TaggedItem

admin.site.register(TaggedItem)
admin.site.register(Tag)
