import json
from random import choice
from string import ascii_uppercase

import requests
from django.utils import timezone

from Cart.models import Order, Item, Delivery, Payment, Status
from Derevo116.settings import TG_TOKEN, TG_CHAT_ID
from Product.models import Product


def prepare_cart(request):
    """обрабатывает данные из сессии и возвращает их в виде словаря для шаблона"""

    cart_count = 0      # количество товаров в корзине
    cart_sum = 0        # сумма всей корзины
    items = {}          # товары в корзине
    order_data = {}     # данные о заказе (оплата, доставка, и т.п.)

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
    """Генерирует номер заказа.
    Год + месяц + случайные символы + максимальный id заказа со сдвигом (+365)"""
    rnd = ''.join(choice(ascii_uppercase) for i in range(3))
    try:
        max_id = Order.objects.latest('id').id + 365
    except:
        max_id = 365
    order_number = f'{timezone.now().strftime("%Y")}-{rnd}-{max_id}'

    return order_number


def send_telegram_message(new_order, item_list):
    """отправляет сообщение в телеграм бот
    ::new_order:: Заказ, который нужно отправить
    item_list: Список товаров"""
    tg_message = f'Новый заказ с сайта derevo116.ru %0A%0A' \
                 f'Номер: {new_order.order_number}%0A' \
                 f'Дата: {timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%m")}%0A%0A' \
                 f'Имя: {new_order.order_client_name}%0A' \
                 f'Телефон: {new_order.order_phone}%0A%0A' \
                 f'Доставка: {new_order.order_delivery}%0A' \
                 f'Оплата: {new_order.order_payment}%0A%0A' \
                 f'Товары :%0A{item_list}%0A' \
                 f'Сумма: {new_order.order_sum}%0A%0A' \
                 f'http://derevo116.ru/admin/Cart/order/{new_order.id}/change/'
    link = f'https://api.telegram.org/bot{TG_TOKEN}/sendmessage?chat_id={TG_CHAT_ID}&text={tg_message}'
    return requests.get(link)


def create_new_order(request, telegram=True):
    """Создает Новый заказ в БД.
    Если telegram=True то отправляет сообщение в телеграм бот"""
    data = json.loads(request.body)

    order_number = generate_order_number()

    request.session.setdefault('order_extra', {})
    request.session['order_extra'] = data
    request.session['order_extra']['order_number'] = order_number

    new_order = Order.objects.create(
        order_number=order_number,
        order_delivery=Delivery.objects.filter(id=request.session['order_data']['orderDeliveryWay']).first(),
        order_delivery_other=request.session['order_data']['orderDeliveryWayText'],
        order_payment=Payment.objects.get(id=request.session['order_data']['orderPay']),
        order_status=Status.objects.get(status_default=1),
        order_history=f"{timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%m')}  -  cтатус: {Status.objects.get(status_default=1)}",
        order_comment=request.session['order_data']['orderComment'],
        order_comment_admin="",
        order_country_city_index=request.session['order_data']['orderDeliveryCountryAndCity'],
        order_address=request.session['order_data']['orderDeliveryAddress'],
        order_client_name=request.session['order_data']['orderDeliveryContact'],
        order_phone=request.session['order_data']['orderDeliveryContactPhone'],
        order_notification=request.session['order_extra']['order_notification'],
        order_email=request.session['order_extra']['order_email'],
        order_call_me=request.session['order_extra']['order_call_me'],
        order_sum=sum(int(request.session['products'][item]['price']) *
                      int(request.session['products'][item]['count'])
                      for item in request.session['products'])
    )

    item_list = ""
    for key, value in request.session['products'].items():
        new_item = Item.objects.create(
            item_product=Product.objects.get(id=value['id']),
            item_id=key,
            item_color=value['color'],
            item_options=value['options'],
            item_price=value['price'],
            item_count=value['count'],
            item_sale=0,
            item_sum=value['sum'],
            item_order=Order.objects.get(order_number=order_number),
        )
        item_list = "".join(value['title'] + '%0A')

    if telegram:
        send_telegram_message(new_order, item_list)