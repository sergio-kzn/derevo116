import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from Cart.models import Country, City, Delivery, Payment, Order
from Cart.services import prepare_cart, create_new_order
from Product.models import Product, Color


def cart(request):
    """Страница Корзина с товарами"""
    if 'products' in request.session:
        for item in request.session['products']:
            product_id = request.session['products'][item]['id']
            product = Product.objects.get(id=product_id)
            request.session['products'][item]['img'] = str(product.product_img)
            request.session['products'][item]['vendor'] = product.product_vendor.vendor_title
            request.session['products'][item]['vendor_code'] = product.product_vendor_code
            if 'color' in request.session['products'][item]:
                colors = Color.objects.filter(color_group__product__id=product_id)
                for color in colors:
                    if color.color_title == request.session['products'][item]['color']:
                        request.session['products'][item]['color_img'] = str(color.color_image)
            request.session['products'][item]['sum'] = int(request.session['products'][item]['price']) * int(
                request.session['products'][item]['count'])
        request.session.modified = True
    content = prepare_cart(request)

    country = Country.objects.all()
    city = City.objects.all()
    delivery = Delivery.objects.filter(delivery_enable=True).filter(delivery_pickup=False)
    pickup = Delivery.objects.filter(delivery_pickup=True).filter(delivery_enable=True)
    # payment = Payment.objects.filter(payment_enable=True)
    content['countries'] = country
    content['cities'] = city
    content['delivery'] = delivery
    content['pickup'] = pickup
    # content['payment'] = payment

    return render(request, 'cart/cart.html', content)


@csrf_exempt
def confirm(request):
    if request.method == 'POST':
        order_data = json.loads(request.body)

        request.session.setdefault('order_data', {})
        request.session['order_data'] = order_data
        request.session.modified = True

        return HttpResponse('OK')
    else:
        content = prepare_cart(request)

        if 'order_data' in request.session:
            delivery = Delivery.objects.get(delivery_API=request.session['order_data']['orderDeliveryWay'])
            payment = Payment.objects.get(payment_API=request.session['order_data']['orderPay'])
            content['delivery'] = delivery
            content['payment'] = payment

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
            else: # print('Нет такого товара')
                request.session['products'][id_item] = product_data
        except KeyError: # print('корзина была пуста')
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


@csrf_exempt
def select_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment = Payment.objects.filter(payment_delivery__delivery_API__exact=data['orderDeliveryWay']).filter(payment_enable=True)
        html = render_to_string('cart/payments.html', {'payment': payment})
        return HttpResponse(html)


@csrf_exempt
def success(request):
    """страница успешного оформления заказа"""
    if request.method == 'POST':
        create_new_order(request)
        return HttpResponse('ok')
    else:
        order_number = request.session['order_extra']['order_number']
        content = {'order_number': order_number}

        request.session.flush()
        return render(request, 'cart/success.html', content)


def search_order(request):
    order = ""
    if request.GET.__contains__('q'):
        try:
            order = Order.objects.get(order_number=request.GET['q'])
        except:
            pass

    if request.GET.__contains__('p'):
        try:
            order = Order.objects.get(order_phone=request.GET['p'])
        except:
            pass

    content = {
        'search': request.GET.get('q', default=None),
        'search_phone': request.GET.get('p', default=None),
        'order': order,
    }
    return render(request, 'cart/search_order.html', content)
