def prepare_cart(request):
    cart_count = 0
    cart_sum = 0

    if len(request.session['products'].values()) < 1:
        items = {}

    if 'products' in request.session:
        items = request.session['products'].items()
        cart_count = len(request.session['products'].values())
        cart_sum = sum(int(request.session['products'][item]['price']) * int(request.session['products'][item]['count']) for item in request.session['products'])
    else:
        items = {}

    content = {
        'cart_item': items,
        'cart_count': cart_count,
        'cart_sum': cart_sum,
    }
    return content