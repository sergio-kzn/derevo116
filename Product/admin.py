from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteInplaceWidget

from .models import ProductCategory, Product, ProductVolumePrice, ProductAttribute, Volume, Color, \
    ColorGroup, ProductVendor, ProductTab


class ProductCategoryList(admin.TabularInline):
    model = ProductCategory
    extra = 0

class ProductCategoryAdmin(admin.ModelAdmin):

    def category_name(self, obj):
        if obj.category_parent:
            return mark_safe(f'{obj.category_parent.category_title} -- {obj.category_title}')
        else:
            return mark_safe(obj.category_title)
    category_name.short_description = 'Категория'

    list_display = ['category_name', 'category_sort', 'category_main_menu']
    inlines = [ProductCategoryList]


class PriceInline(admin.TabularInline):
    model = ProductVolumePrice
    extra = 5

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PriceInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'volumeprice_price' or db_field.name == 'volumeprice_expenditure' or db_field.name == 'volumeprice_expenditure_price':
            field.widget.attrs['style'] = 'width: 10em;'
        return field


class AttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 5


class ColorInline(admin.TabularInline):
    model = Color
    extra = 0
    field = ['color_title', 'image_preview', 'color_image', 'color_sort']

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """либо показывает изображение в поле Обзор, либо пишет No image"""
        if obj.color_image:
            return mark_safe('<img src="{0}" width="160" height="65" style="object-fit:contain" />'.format(obj.color_image.url))
        else:
            return '(No image)'
    image_preview.short_description = 'Просмотр'



class ProductAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    inlines = [PriceInline, AttributeInline]
    list_display = ['image_preview', 'product_title', 'product_category_with_html', 'product_vendor_code', 'product_link']
    list_filter = ['product_vendor', 'product_show']
    fieldsets = (
        (None, {
            'fields': ('product_show',
                       'product_category',
                       ('product_vendor', 'product_vendor_code'),
                       'product_title',
                       'product_url',
                       'product_content',
                       'product_count',

                       )
        }),
        ('Изображение', {
            'classes': ('collapse',),
            'fields': (('image_preview', 'product_img'),
                       ),
        }),
        ('Дополнительно', {
            'classes': ('collapse',),
            'fields': ('product_file',
                       'product_extra_desc',
                       'product_color',
                       'product_tab'),
        }),
        ('Цена', {
            'classes': ('collapse',),
            'fields': ('product_price_choice',
                       'product_price',
                       'product_price_title_1',
                       'product_price_title_2',
                       'product_price_title_3',
                       'product_price_title_4',)
        })
    )
    save_on_top = True
    list_display_links = ['image_preview', 'product_title']

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ProductAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'product_title':
            field.widget.attrs['style'] = 'display: flex; width: -webkit-fill-available;'
        return field

    def product_link(self, obj):
        if obj.product_url:
            vendor_link = obj.product_vendor.vendor_url
            category_link = f'{obj.product_category.category_url}'
            product_link = f'{obj.product_url}'
            url = reverse('product', args=(vendor_link, category_link, product_link,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.product_url}</a>')
        else:
            return '(No link)'
    product_link.short_description = 'Ссылка'

    readonly_fields = ('image_preview',)
    def image_preview(self, obj):
        """либо показывает изображение в поле Обзор, либо пишет No image"""
        if obj.product_img:
            return mark_safe('<img src="{0}" width="160" height="65" style="object-fit:contain" />'.format(obj.product_img.url))
        else:
            return '(No image)'
    image_preview.short_description = 'Просмотр'

    def product_category_with_html(self, obj):
        if obj.product_category:
            return mark_safe(obj.product_category)
    product_category_with_html.short_description = 'Категория'


class VolumeAdmin(admin.ModelAdmin):
    """так выглядит раздел с Опциями цены в админке"""
    list_display = ['volume_title', 'volume_sort']
    list_editable = ['volume_sort']


class ColorAdmin(admin.ModelAdmin):
    """так выглядит раздел с Цветом в админке
    еще тут есть функция, которая делает превью загруженной картинки."""
    inlines = [ColorInline]


class TabAdmin(SummernoteModelAdmin):
    summernote_fields = "__all__"
    list_display = ['tab_title_admin', 'tab_title', 'tab_slug']



admin.site.register(ProductCategory, ProductCategoryAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(ColorGroup, ColorAdmin)
admin.site.register(ProductVendor)
admin.site.register(ProductTab, TabAdmin)
