from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ProductCategory, Product


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

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product)
