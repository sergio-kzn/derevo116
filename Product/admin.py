from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from fieldsets_with_inlines import FieldsetsInlineMixin

from .models import ProductCategory, Product, ProductOptionPrice, ProductAttribute, Color, \
    ColorGroup, ProductVendor, ProductTab, ProductImage, ProductImageGroup, OptionGroup, OptionPrice


class RefererFilter(admin.SimpleListFilter):
    """Новый фильтр для Опций цен. Показыавет установлена какая либо опция или нет"""

    title = 'Опции цен'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'product_price_options'

    def lookups(self, request, model_admin):
        return (
            ('False', 'Товары с опциями'),
            ('True', 'Товары без опций'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'False':
            return queryset.filter(product_price_options__isnull=False)
        if self.value() == 'True':
            return queryset.filter(product_price_options__isnull=True)


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
    list_editable = ['category_sort', 'category_main_menu']
    inlines = [ProductCategoryList]


class AttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 5
    classes = ['collapse']


class ColorInline(admin.TabularInline):
    model = Color
    extra = 0
    fields = ['color_title', 'image_preview', 'color_image', 'color_sort']
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """либо показывает изображение в поле Обзор, либо пишет No image"""
        if obj.color_image:
            return mark_safe(
                '<img src="{0}" width="160" height="65" style="object-fit:contain" />'.format(obj.color_image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Просмотр'


class ColorAdmin(admin.ModelAdmin):
    inlines = [ColorInline]


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ['img_file', 'image_preview', 'img_title']
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """либо показывает изображение в поле Обзор, либо пишет No image"""
        if obj.img_file:
            return mark_safe(
                '<img src="{0}" width="100" height="100" style="object-fit:contain" />'.format(obj.img_file.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Просмотр'


class ImageAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['img_group', 'count_image']

    def count_image(self, obj):
        return ProductImage.objects.filter(img_group=obj).count()

    count_image.short_description = 'Кол-во'


class ProductAdmin(FieldsetsInlineMixin, SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    list_display = ['image_preview', 'product_title', 'product_category_with_html', 'product_vendor_code',
                    'product_link']
    list_filter = ['product_vendor', 'product_show', 'product_price_choice', RefererFilter, 'product_count']
    filter_horizontal = ['product_images', 'product_color', 'product_tab', 'product_price_options']
    fieldsets_with_inlines = (
        (None, {
            'fields': ('product_show',
                       'product_link',
                       'product_category',
                       'product_vendor',
                       'product_vendor_code',
                       'product_title',
                       'product_url',
                       'product_count',
                       )
        }),
        ('Описание', {
            'classes': ('collapse',),
            'fields': ('product_extra_desc',
                       'product_content',
                       ),
        }),
        AttributeInline,
        (None, {
            'fields': ('help_attr',)
        }),
        ('Изображение', {
            'classes': ('collapse',),
            'fields': (('image_preview', 'product_img'),
                       'product_img_title',
                       'product_images',
                       ),
        }),
        ('Дополнительно', {
            'classes': ('collapse',),
            'fields': ('product_file',
                       'product_tab'),
        }),
        ('Цена', {
            # 'classes': ('collapse',),
            'fields': ('product_price_choice',
                       'product_price',
                       'product_color',
                       'product_price_options',
                       )
        })
    )
    save_on_top = True
    list_display_links = ['image_preview', 'product_title']
    readonly_fields = ('image_preview', 'product_link', 'help_attr')
    # prepopulated_fields = {"product_price_options.option_group": ("product_title",)}
    radio_fields = {"product_price_choice": admin.VERTICAL}

    def help_attr(self, obj):
        return '<sup>2</sup>\n<sup>3</sup>\n°C'

    help_attr.short_description = 'Подсказки для копирования'

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ProductAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'product_title':
            field.widget.attrs['style'] = 'display: flex; width: -webkit-fill-available;'
        if db_field.name == 'product_img_title':
            field.widget.attrs['style'] = 'display: flex; width: -webkit-fill-available;'

        return field

    def product_link(self, obj):
        if obj.product_url:
            vendor_link = obj.product_vendor.vendor_url
            category_link = f'{obj.product_category.category_url}'
            product_link = f'{obj.product_url}'
            url = reverse('product', args=(vendor_link, category_link, product_link,))
            return mark_safe(f'<a href="{url}" target="_blank"><i class="fas fa-external-link-alt fa-2x"></i></i></a>')
        else:
            return '(No link)'

    product_link.short_description = 'Перейти'

    def image_preview(self, obj):
        """либо показывает изображение в поле Обзор, либо пишет No image"""
        if obj.product_img:
            return mark_safe(
                '<img src="{0}" width="160" height="65" style="object-fit:contain" />'.format(obj.product_img.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Просмотр'

    def product_category_with_html(self, obj):
        if obj.product_category:
            return mark_safe(obj.product_category)

    product_category_with_html.short_description = 'Категория'

    class Media:
        css = {
            'all': ('css/all.min.css',)
        }


class OptionGroupInlines(admin.TabularInline):
    model = ProductOptionPrice
    extra = 5

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(OptionGroupInlines, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'product_option_extra_2' or db_field.name == 'product_option_price'\
                or db_field.name == 'product_option_extra_1':
            field.widget.attrs['style'] = 'width: 10em;'
        return field


class OptionGroupAdmin(admin.ModelAdmin):
    """так выглядит раздел с Опциями в админке"""
    list_display = ['option_group', 'option_type']
    inlines = [OptionGroupInlines]


class TabAdmin(SummernoteModelAdmin):
    """Дополнительные вкладки в админке"""
    summernote_fields = "__all__"
    list_display = ['tab_title_admin', 'tab_title', 'tab_slug']


class VendorAdmin(admin.ModelAdmin):
    """раздел с поставщиками в админке"""
    list_display = ['vendor_title', 'vendor_sort']
    list_editable = ['vendor_sort']


class OptionPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'option_title', 'option_sort']
    list_editable = ['option_title', 'option_sort']
    fields = ['option_title', 'option_sort']
    readonly_fields = ['id']


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(OptionPrice, OptionPriceAdmin)
admin.site.register(ColorGroup, ColorAdmin)
admin.site.register(ProductImageGroup, ImageAdmin)
admin.site.register(ProductVendor, VendorAdmin)
admin.site.register(ProductTab, TabAdmin)
