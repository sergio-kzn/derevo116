from Product.models import ProductOptionPrice as Price
from loguru import logger


def update_price(dict):
    # {'306': {'new_price': '539', 'new_price_rate': '216  /  359'},
    #  '307': {'new_price': '1 507', 'new_price_rate': '201  /  343'},
    #  '308': {'new_price': '3 740', 'new_price_rate': '187  /  288'},
    #  '309': {'new_price': '8 872', 'new_price_rate': '177  /  277'}}
    logger.add("file_1.log", rotation="500 MB", format="{time} {level} {message}")
    for id in dict:
        price = Price.objects.get(id=id)

        logger.info('id={} | old price={}', price.id, price.product_option_price)
        logger.info('id={} | old price_rate={}', price.id, price.product_option_extra_2)

        price.product_option_price = dict[id]['new_price']

        if dict[id]['new_price_rate'] == 'None':
            price.product_option_extra_2 = None
        else:
            price.product_option_extra_2 = dict[id]['new_price_rate']

        price.save()

        logger.info('id={} | new price={}', price.id, price.product_option_price)
        logger.info('id={} | new price_rate={}', price.id, price.product_option_extra_2)


    return True