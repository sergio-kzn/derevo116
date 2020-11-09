from django import template

from Cart.services import prepare_cart

register = template.Library()


@register.inclusion_tag('cart_tag.html', takes_context=True)
def cart_tag(context):
    request = context['request']
    return prepare_cart(request)
