from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin
from django.utils.safestring import mark_safe

from .models import Slide, Group



class SlideInline(admin.StackedInline, SummernoteInlineModelAdmin):
    model = Slide
    extra = 0
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # slider_img - поле с изображением
        if obj.slide_img:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.slide_img.url))
        else:
            return '(No image)'
    image_preview.short_description = 'Просмотр'
    summernote_fields = '__all__'



class GroupAdmin(admin.ModelAdmin):
    inlines = [SlideInline]


class SlideAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


admin.site.register(Group, GroupAdmin)
admin.site.register(Slide, SlideAdmin)