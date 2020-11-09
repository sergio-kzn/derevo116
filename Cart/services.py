def prepare_cart(request):
    cart_count = 0
    cart_sum = 0
    if 'products' in request.session:
        items = request.session['products'].values()
        cart_count = len(items)
        print(items)
        cart_sum = sum(int(request.session['products'][item]['price']) * int(request.session['products'][item]['count']) for item in request.session['products'])
    else:
        items = {}

    #
    # if 'cart_sum' in request.session:
    #     cart_sum = request.session['cart_sum']
    # else:
    #     cart_sum = 0

    content = {
        'cart_item': items,
        'cart_count': cart_count,
        'cart_sum': cart_sum,
    }
    return content