from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from SimplePage.models import SimplePage


class SimplePageAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ['simple_page_title', 'simple_page_link']

    def simple_page_link(self, obj):
        if obj.simple_page_url:
            return mark_safe(f'<a href="/page/{obj.simple_page_url}" target="_blank">{obj.simple_page_url}</a>')
        else:
            return '(No link)'
    simple_page_link.short_description = 'Ссылка'

admin.site.register(SimplePage, SimplePageAdmin)
