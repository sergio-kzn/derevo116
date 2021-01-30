from functools import lru_cache

from django import template
from Product.models import ProductCategory

register = template.Library()

@register.inclusion_tag('categories.html')
@lru_cache
def categories(main_menu_filter=1):
    """ Загрузка категорий из БД Биофа
    FIXME: Сделать запуск через крон раз в сутки"""
    print(categories.cache_info())
    return {'categories': ProductCategory.objects.filter(category_main_menu=bool(main_menu_filter))}
