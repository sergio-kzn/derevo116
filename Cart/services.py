def prepare_cart(request):
    cart_count = 0
    cart_sum = 0
    items = {}
    order_data = {}

    if 'products' in request.session:
        items = request.session['products'].items()
        cart_count = len(request.session['products'].values())
        cart_sum = sum(int(request.session['products'][item]['price']) * int(request.session['products'][item]['count']) for item in request.session['products'])

    if 'order_data' in request.session:
        order_data = request.session['order_data']

    content = {
        'order_data': order_data,
        'cart_item': items,
        'cart_count': cart_count,
        'cart_sum': cart_sum,
    }
    return content
