from django.contrib import admin
from .models import Keyword, ContentItem, Flag


class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'last_updated')


admin.site.register(Keyword)
admin.site.register(ContentItem, ContentItemAdmin)
admin.site.register(Flag)