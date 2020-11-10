import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from Cart.services import prepare_cart
from Product.models import Product, Color


def cart(request):
    """Страница Корзина с товарами"""
    for item in request.session['products']:
        product = Product.objects.get(id=request.session['products'][item]['id'])
        request.session['products'][item]['img'] = str(product.product_img)
        request.session['products'][item]['vendor'] = product.product_vendor.vendor_title
        request.session['products'][item]['vendor_code'] = product.product_vendor_code
        if 'color' in request.session['products'][item]:
            colors = Color.objects.filter(color_group__product__id=request.session['products'][item]['id'])
            for color in colors:
                if color.color_title == request.session['products'][item]['color']:
                    request.session['products'][item]['color_img'] = str(color.color_image)
        request.session['products'][item]['sum'] = int(request.session['products'][item]['price']) * int(
            request.session['products'][item]['count'])

    request.session.modified = True
    content = prepare_cart(request)
    return render(request, 'cart/cart.html', content)


@csrf_exempt
def confirm(request):
    if request.method == 'POST':
        order_data = json.loads(request.body)

        request.session.setdefault('order_data', order_data)
        # request.session.setdefault('order_data', {
        #     'orderComment': order_data['orderComment'],
        #     'orderDelivery': order_data['orderDelivery'],
        #     'orderDeliveryWay': order_data['orderDeliveryWay'],
        #     'orderDeliveryWayText': order_data['orderDeliveryWayText'],
        #     'orderPay': order_data['orderPay'],
        #     'orderDeliveryCountryAndCity': order_data['orderDeliveryCountryAndCity'],
        #     'orderDeliveryAdress': order_data['orderDeliveryAdress'],
        #     'orderDeliveryContact': order_data['orderDeliveryContact'],
        #     'orderDeliveryContactPhone': order_data['orderDeliveryContactPhone'],
        # })
        # request.session['order_data']['orderComment'] = order_data['orderComment']
        request.session.modified = True

        return HttpResponse('OK')
    else:
        content = prepare_cart(request)
        return render(request, 'cart/confirm.html', content)


@csrf_exempt
def add_to_cart(request):
    """добавление товара в корзину"""
    if request.method == 'POST':
        product_data = json.loads(request.body)
        id_item = f'{product_data["id"]}-{product_data["color"]}-{product_data["options"]}'
        try:
            if id_item in request.session['products']:  # print('Уже есть такой товар')
                request.session['products'][id_item]['count'] = int(
                    request.session['products'][id_item]['count']) + int(product_data['count'])
            else:
                print('Нет такого товара')
                request.session['products'][id_item] = product_data
        except KeyError:
            print('корзина была пуста')
            request.session.setdefault('products', {id_item: product_data})
            # request.session['products'][id_item] = product_data

        request.session.modified = True
        html = render_to_string('cart_tag.html', prepare_cart(request))
        return HttpResponse(html)

@csrf_exempt
def delete_from_cart(request):
    """удалить товар из корзины"""
    if request.method == 'POST':
        product_data = json.loads(request.body)
        id_item = product_data["key"]
        del request.session['products'][id_item]
        request.session.modified = True

        html = render_to_string('cart_tag.html', prepare_cart(request))
        return HttpResponse(html)


@csrf_exempt
def clear_cart(request):
    """очистка корзины"""
    request.session.flush()
    return redirect(request.META['HTTP_REFERER'])


def success(request):
    """очистка корзины"""
    request.session.flush()
    content = {}
    return render(request, 'cart/success.html', content)
