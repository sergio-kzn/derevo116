from django import template
from Product.models import ProductCategory

register = template.Library()


@register.inclusion_tag('categories.html')
def categories():
    """ Загрузка категорий из БД Биофа
    FIXME: Сделать запуск через крон раз в сутки"""

    return {'categories': ProductCategory.objects.filter(category_main_menu=True)}
