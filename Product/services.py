import random

from Product.models import Product


def random_relevant_products(product_id):
    items_in_category_max = 5
    items_in_vendor_max = 5
    total_items = 5

    category_url = Product.objects.get(id=product_id).product_category.category_url
    vendor_url = Product.objects.get(id=product_id).product_vendor.vendor_url
    items_in_category = Product.objects.filter(product_category__category_url=category_url, product_show=True).exclude(id=product_id).values('id')
    items_in_vendor = Product.objects.filter(product_vendor__vendor_url=vendor_url, product_show=True).exclude(product_category__category_url=category_url)


    items_in_category_list = list()
    for item in items_in_category:
        items_in_category_list.append(item['id'])

    items_in_vendor_list = list()
    for item in items_in_vendor:
        items_in_vendor_list.append(item.id)


    if items_in_category_max > len(items_in_category_list):
        items_in_category_max = len(items_in_category_list)
    if items_in_vendor_max > len(items_in_vendor_list):
        items_in_vendor_max = len(items_in_vendor_list)

    if len(items_in_category_list) >= 3 and len(items_in_vendor_list) >=2:
        items_in_category_max = 3
        items_in_vendor_max = 2

    items_in_category_list_random = random.sample(items_in_category_list, items_in_category_max)
    items_in_vendor_list_random = random.sample(items_in_vendor_list, items_in_vendor_max)

    random_items = list()
    random_items.extend(items_in_category_list_random)
    random_items.extend(items_in_vendor_list_random)
    random_items = random_items[:total_items]

    products = Product.objects.filter(id__in=random_items).order_by('product_category__category_sort', 'product_category')
    return products