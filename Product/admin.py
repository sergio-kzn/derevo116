from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from fieldsets_with_inlines import FieldsetsInlineMixin

from .models import ProductCategory, Product, ProductOptionPrice, ProductAttribute, Color, \
    ColorGroup, ProductVendor, ProductTab, ProductImage, ProductImageGroup, OptionGroup, OptionPrice


class OptionPriceFilter(admin.SimpleListFilter):
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


class ColorFilter(admin.SimpleListFilter):
    """Фильтр для Цвета. Показыавет установлены ли цвета для товара"""

    title = 'Выбор цвета'
    parameter_name = 'product_color'

    def lookups(self, request, model_admin):
        return (
            ('False', 'Товары с выбором Цвета'),
            ('True', 'Товары без выбора Цвета'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'False':
            return queryset.filter(product_color__isnull=False)
        if self.value() == 'True':
            return queryset.filter(product_color__isnull=True)


class ProductCategoryList(admin.TabularInline):
    model = ProductCategory
    extra = 0


class ProductCategoryAdmin(admin.ModelAdmin):
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
    fields = ['color_image', 'image_preview', 'color_html', 'color_title', 'color_sort']
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """либо показывает изображение в поле Обзор, либо пишет No image"""
        if obj.color_image:
            return mark_safe(
                '<img src="{0}" width="160" height="65" style="object-fit:contain" />'.format(obj.color_image.url))
        elif obj.color_html:
            return mark_safe(
                '<div style="width:160px; height:65px; background-color: {0}">'.format(obj.color_html))
        else:
            return '(No image)'

    image_preview.short_description = 'Просмотр'

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ColorInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'color_html':
            field.widget.attrs['style'] = 'width: 10em;'
        return field


class ColorAdmin(admin.ModelAdmin):
    inlines = [ColorInline]
    list_display = ['color_group_name', 'count_color']
    readonly_fields = ['count_color']

    def count_color(self, obj):
        return Color.objects.filter(color_group=obj).count()

    count_color.short_description = 'Кол-во'

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ColorAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'color_group_name':
            field.widget.attrs['style'] = 'display: flex; width: -webkit-fill-available;'
        if db_field.name == 'color_group_title':
            field.widget.attrs['style'] = 'display: flex; width: -webkit-fill-available;'
        return field


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ['img_file', 'image_preview', 'img_title', 'img_sort']
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
    list_display = ['img_group', 'count_image', 'img_group_sort']
    ordering = ['-id']
    readonly_fields = ['id']

    def count_image(self, obj):
        return ProductImage.objects.filter(img_group=obj).count()

    count_image.short_description = 'Кол-во'


class ProductAdmin(FieldsetsInlineMixin, SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    list_display = ['image_preview', 'product_title', 'product_category_with_html', 'product_vendor_code',
                    'product_link']
    list_filter = ['product_vendor', 'product_show', 'product_price_choice', OptionPriceFilter, ColorFilter,
                   'product_count']
    filter_horizontal = ['product_images', 'product_color', 'product_tab', 'product_price_options']
    save_on_top = True
    list_display_links = ['image_preview', 'product_title']
    readonly_fields = ('image_preview', 'product_link', 'fill_url', 'help_attr', 'fill_img_title', 'edit_images',
                       'copy_url', 'edit_colors', 'edit_tabs', 'edit_options')
    radio_fields = {"product_price_choice": admin.VERTICAL}
    list_per_page = 20
    fieldsets_with_inlines = (
        (None, {
            'fields': ('product_show',
                       'product_link',
                       'product_category',
                       'product_vendor',
                       'product_vendor_code',
                       'product_title',
                       ('product_url', 'fill_url'),
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
                       ('product_img_title', 'fill_img_title'),
                       'product_images',
                       'edit_images',
                       ),
        }),
        ('Дополнительно', {
            'classes': ('collapse',),
            'fields': (('product_file', 'copy_url'),
                       'product_tab',
                       'edit_tabs'),
        }),
        ('Цена', {
            # 'classes': ('collapse',),
            'fields': ('product_price_choice',
                       'product_price',
                       'product_color',
                       'edit_colors',
                       'product_price_options',
                       'edit_options',
                       )
        })
    )

    def fill_url(self, obj):
        """добавляет кнопку для автоматического заполнения поля URL. Артикул + поставщик"""
        snap = '<snap style="cursor: pointer" class="text-primary" onclick="' \
               'let vendor = Array.from(id_product_vendor.options).' \
               'filter(option => option.selected).map(option => option.textContent);' \
               'let code = id_product_vendor_code.value;' \
               'let url_input = document.getElementById(\'id_product_url\');' \
               'let slug = (code + \'-\' + vendor).toLowerCase().replace(/\\s+/g, \'-\');' \
               'url_input.value = slug;' \
               '">Заполнить (артикул-поставщик)</snap>'
        return mark_safe(snap)

    def fill_img_title(self, obj):
        snap = '<snap style="cursor: pointer" class="text-primary" onclick="' \
               'let title = id_product_title.value;' \
               'id_product_img_title.value = title;' \
               '">' \
               'Заполнить это поле из названия</snap><br>' \
               '<span class="text-primary" style="cursor:pointer;" ' \
               'onclick="if (navigator.clipboard) navigator.clipboard.writeText(id_product_title.value)">' \
               'Копировать название продукта</span>'
        return mark_safe(snap)

    def edit_images(self, obj):
        url = ''
        if obj.product_images.all():
            url += '<div class="list-group list-group-flush">'
            for opt in obj.product_images.all():
                url += '<a href="/admin/Product/productimagegroup/' + \
                       str(opt.id) + \
                       '/change/" target="blank" class="list-group-item list-group-item-action">' + \
                       opt.img_group + \
                       '</a><br>'
            url += '</div>'

        return mark_safe(url)

    def edit_tabs(self, obj):
        url = ''
        if obj.product_tab.all():
            url += '<div class="list-group list-group-flush">'
            for opt in obj.product_tab.all():
                url += '<a href="/admin/Product/producttab/' + \
                       str(opt.id) + \
                       '/change/" target="blank" class="list-group-item list-group-item-action">' + \
                       opt.tab_title_admin + \
                       '</a><br>'
            url += '</div>'

        return mark_safe(url)

    def edit_colors(self, obj):
        url = ''
        if obj.product_color.all():
            url += '<div class="list-group list-group-flush">'
            for opt in obj.product_color.all():
                url += '<a href="/admin/Product/colorgroup/' + \
                       str(opt.id) + \
                       '/change/" target="blank" class="list-group-item list-group-item-action">' + \
                       opt.color_group_name + \
                       '</a><br>'
            url += '</div>'

        return mark_safe(url)

    def edit_options(self, obj):
        url = ''
        if obj.product_vendor_code:
            url += '<p>Артикул:<br>' + obj.product_vendor_code + '</p>'
        if obj.product_title:
            url += '<p>Название:<br>' + \
                   obj.product_title + \
                   '  <span class="text-primary" onclick="' \
                   'if (navigator.clipboard) navigator.clipboard.writeText(\'' + \
                   obj.product_title + \
                   '\')" style="cursor:pointer;">(copy)</span></p>'
        if obj.product_images.all():
            count = 0
            for img in obj.product_images.all():
                count += img.productimage_set.all().count()
            url += '<p>Доп. изображения: ' + str(count) + '</p>'
        if obj.product_price_options.all():
            url += '<p>Опции:</p><div class="list-group list-group-flush">'
            for opt in obj.product_price_options.all():
                url += '<a href="/admin/Product/optiongroup/' + \
                       str(opt.id) + \
                       '/change/" target="blank" class="list-group-item list-group-item-action">' + \
                       opt.option_group + '</a>'
            url += '</div>'

        return mark_safe(url)

    def help_attr(self, obj):
        """Добавляет подсказки для атрибутов."""
        if obj.product_category:

            category = obj.product_category

            attributes = set()
            for attribute in ProductAttribute.objects.filter(attribute_product__product_category=category).exclude(
                    attribute_title=None):
                attributes.add(str(attribute))

            total_attr = str(len(attributes))
            url = '<span class="text-primary" style="cursor:pointer;" ' \
                  'onclick=\'let total_forms = document.getElementById("id_productattribute_set-TOTAL_FORMS");' \
                  'if (total_forms >= ' + total_attr + ') console.log(total_forms);' \
                                                       'let attributes = [' + ','.join(
                '"{0}"'.format(a) for a in attributes) + '];' \
                                                         'let input;' \
                                                         'for (let i = 0; i <= ' + total_attr + '; i++) {' \
                                                                                                'input = document.getElementById("id_productattribute_set-"+ i +"-attribute_title");' \
                                                                                                'input.value = attributes[i];' \
                                                                                                'document.getElementById("attribute_title_count").textContent = "Заполнено " + (i+1) + " из ' + total_attr + '"' \
                                                                                                '}' \
                                                                                                '\'>Заполнить</span><br><span id="attribute_title_count"></span>'

            return mark_safe(url)
                # '<sup>2</sup>\n<sup>3</sup>\n°C'
        else:
            return 'Выберите категорию и сохраните товар'

    def copy_url(self, obj):
        snap = '<span class="text-primary" style="cursor:pointer;" ' \
               'onclick="if (navigator.clipboard) navigator.clipboard.writeText(id_product_url.value)">' \
               'Копировать URL продукта</span>'
        return mark_safe(snap)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Добавляем стили для полей в админке"""
        field = super(ProductAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'product_title':
            field.widget.attrs['style'] = 'display: flex; width: -webkit-fill-available;'
        if db_field.name == 'product_img_title':
            field.widget.attrs['style'] = 'display: flex; width: -webkit-fill-available;'
        return field

    def product_link(self, obj):
        if obj.product_url:
            try:
                product_link = obj.product_url
                category_link = obj.product_category.category_url
                vendor_link = obj.product_category.category_parent.category_url
                root_link = obj.product_category.category_parent.category_parent.category_url
                url = reverse('product-url', args=(root_link, vendor_link, category_link, product_link,))
                return mark_safe(
                    f'<a href="{url}" target="_blank"><i class="fas fa-external-link-alt fa-2x"></i></i></a>')
            except:
                pass
        else:
            return '(No link)'

    def image_preview(self, obj):
        """либо показывает изображение в поле Обзор, либо пишет No image"""
        if obj.product_img:
            return mark_safe(
                '<img src="{0}" width="160" height="65" style="object-fit:contain" />'.format(obj.product_img.url))
        else:
            return '(No image)'

    def product_category_with_html(self, obj):
        if obj.product_category:
            return mark_safe(obj.product_category)

    image_preview.short_description = 'Изображение'
    product_category_with_html.short_description = 'Категория'
    fill_url.short_description = ""
    fill_img_title.short_description = ""
    edit_options.short_description = "Дополнительно"
    help_attr.short_description = 'Заполнить атрибуты из других товаров в этой категории'
    copy_url.short_description = ''
    product_link.short_description = 'Перейти'

    class Media:
        css = {
            'all': ('css/all.min.css', 'css/admin.css')
        }


class OptionGroupInlines(admin.TabularInline):
    model = ProductOptionPrice
    extra = 5

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(OptionGroupInlines, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'product_option_extra_2' or db_field.name == 'product_option_price' \
                or db_field.name == 'product_option_extra_1':
            field.widget.attrs['style'] = 'width: 10em;'
        return field


class OptionGroupAdmin(admin.ModelAdmin):
    """так выглядит раздел с Опциями в админке"""
    list_display = ['option_group', 'option_type']
    inlines = [OptionGroupInlines]
    # prepopulated_fields = {"option_title": ("product_title",)}
    # radio_fields = {'option_type', admin.VERTICAL}


class TabAdmin(SummernoteModelAdmin):
    """Дополнительные вкладки на странице товаров"""
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
