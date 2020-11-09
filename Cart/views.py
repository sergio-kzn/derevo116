import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from Cart.services import prepare_cart


def cart(request):
    return render(request, 'cart/cart.html')


def confirm(request):
    return render(request, 'cart/confirm.html')

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_data = json.loads(request.body)
        id_item = f'{product_data["id"]}-{product_data["color"]}-{product_data["options"]}'

        request.session['cart_sum'] = 0

        try:
            if id_item in request.session['products']:
                print('Уже есть такой товар')
                request.session['products'][id_item]['count'] = int(request.session['products'][id_item]['count']) + int(product_data['count'])
            else:
                request.session['products'][id_item] = product_data

        except KeyError:
                print('Нет такого товара')
                request.session.setdefault('products', {id_item: product_data})
                request.session['products'][id_item] = product_data

        request.session.modified = True

        html = render_to_string('cart_tag.html', prepare_cart(request))
        return HttpResponse(html)

@csrf_exempt
def clear_cart(request):
    request.session.flush()
    return redirect(request.META['HTTP_REFERER'])
