from random import choice
from string import ascii_uppercase

from django.utils import timezone

from Cart.models import Order


def prepare_cart(request):
    """обрабатывает данные из сессии и возвращает их в виде словаря для шаблона"""

    cart_count = 0
    cart_sum = 0
    items = {}
    order_data = {}

    if 'products' in request.session:
        items = request.session['products'].items()
        cart_count = len(request.session['products'].values())
        cart_sum = sum(int(request.session['products'][item]['price']) *
                       int(request.session['products'][item]['count'])
                       for item in request.session['products'])

    if 'order_data' in request.session:
        order_data = request.session['order_data']

    content = {
        'order_data': order_data,
        'cart_item': items,
        'cart_count': cart_count,
        'cart_sum': cart_sum,
    }

    return content


def generate_order_number():
    rnd = ''.join(choice(ascii_uppercase) for i in range(3))

    try:
        max_id = Order.objects.latest('id').id + 365
    except:
        max_id = 365

    order_number = f'{timezone.now().strftime("%Y%m")}-{rnd}-{max_id}'
    return order_number
