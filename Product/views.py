from django.shortcuts import render

from Product.models import Product, ProductAttribute, ProductCategory, ProductVendor, Color, ProductImage, OptionGroup
from Product.services import random_relevant_products


def product(request, root_url, vendor_url, category_url, product_url):
    root_category = ProductCategory.objects.get(category_url=root_url)
    vendor_category = ProductCategory.objects.get(category_url=vendor_url)
    current_category = ProductCategory.objects.get(category_url=category_url)

    product = Product.objects.get(product_url=product_url)
    price_data = OptionGroup.objects.filter(product__product_url=product_url).order_by('options_sort')
    attributes = ProductAttribute.objects.filter(attribute_product__product_url=product_url)
    colors = Color.objects.filter(color_group__product__product_url=product_url)
    images = ProductImage.objects.filter(img_group__product__product_url=product_url)\
        .order_by('img_group__img_group_sort')

    random_items = random_relevant_products(product.id)

    content = {
        'root_category': root_category,
        'vendor_category': vendor_category,
        'current_category': current_category,

        'product': product,
        'options_price': price_data,
        'attributes': attributes,
        'colors': colors,
        'images': images,
        'random_items': random_items,
    }
    return render(request, 'product/product.html', content)


def category(request, root_url, vendor_url, category_url):
    products = Product.objects.filter(product_show=True).filter(product_category__category_url=category_url)
    root_category = ProductCategory.objects.get(category_url=root_url)
    current_vendor = ProductCategory.objects.get(category_url=vendor_url)
    current_category = ProductCategory.objects.get(category_url=category_url)
    categories = ProductCategory.objects.filter(category_main_menu=True)\
        .filter(category_parent__category_url=vendor_url)

    content = {
        'products': products,
        'root_category': root_category,
        'current_vendor': current_vendor,
        'current_category': current_category,
        'categories': categories,
    }
    return render(request, 'product/category.html', content)


def vendor_category(request, root_url, vendor_url):
    products = Product.objects.filter(product_show=True).filter(product_vendor__vendor_url=vendor_url)
    root_category = ProductCategory.objects.get(category_url=root_url)
    current_vendor = ProductCategory.objects.get(category_url=vendor_url)
    categories = ProductCategory.objects.filter(category_main_menu=True)\
        .filter(category_parent__category_url=vendor_url)

    content = {
        'products': products,
        'root_category': root_category,
        'current_vendor': current_vendor,
        'categories': categories,
    }
    return render(request, 'product/category.html', content)


def root_category(request, root_url):
    root_category = ProductCategory.objects.get(category_url=root_url)
    categories = ProductCategory.objects.filter(category_main_menu=True)

    content = {
        'root_category': root_category,
        'categories': categories,
    }
    return render(request, 'product/category.html', content)
