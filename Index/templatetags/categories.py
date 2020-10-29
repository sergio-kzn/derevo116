from django import template
# from BiofaImportBD.models import ProductCategoryproduct
from Product.models import ProductCategory

register = template.Library()


@register.inclusion_tag('categories.html')
def categories(vendor):
    """ Загрузка категорий из БД Биофа
    FIXME: Сделать запуск через крон раз в сутки"""

    global categories, category_vendor

    categories = ProductCategory.objects.all()
    category_vendor = vendor

    return {
        'categories': categories,
        'vendor': category_vendor,
    }
