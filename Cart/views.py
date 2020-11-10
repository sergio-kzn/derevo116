import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from Cart.services import prepare_cart


def cart(request):
    # product_data = json.loads(request.body)
    content = prepare_cart(request)

    return render(request, 'cart/cart.html', content)


def confirm(request):
    return render(request, 'cart/confirm.html')

@csrf_exempt
def add_to_cart(request):
    """добавление товара в корзину"""
    if request.method == 'POST':
        product_data = json.loads(request.body)
        id_item = f'{product_data["id"]}-{product_data["color"]}-{product_data["options"]}'
        try:
            if id_item in request.session['products']: # print('Уже есть такой товар')
                request.session['products'][id_item]['count'] = int(request.session['products'][id_item]['count']) + int(product_data['count'])
            else: # print('Нет такого товара')
                request.session['products'][id_item] = product_data
        except KeyError: # print('корзина была пуста')
                request.session.setdefault('products', {id_item: product_data})
                request.session['products'][id_item] = product_data
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
