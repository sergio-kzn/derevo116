import random

from django.shortcuts import render

from Product.models import Product, ProductVolumePrice, ProductAttribute, ProductCategory, ProductVendor, Color, \
    ProductImage
from Product.services import random_relevant_products


def product(request, vendor_url, category_url, product_url):
    product = Product.objects.filter(product_url=product_url)[0]
    price_data = ProductVolumePrice.objects.filter(volumeprice_product__product_url=product_url)
    attributes = ProductAttribute.objects.filter(attribute_product__product_url=product_url)
    colors = Color.objects.filter(color_group__product__product_url=product_url)
    images = ProductImage.objects.filter(img_group__product__product_url=product_url)

    random_items = random_relevant_products(product.id)

    content = {
        'product': product,
        'volume_price': price_data,
        'attributes': attributes,
        'colors': colors,
        'images': images,
        'random_items': random_items,
    }
    return render(request, 'product/product.html', content)


def category(request, vendor_url, category_url):
    category = ProductCategory.objects.filter(category_url=category_url)
    all_category = ProductCategory.objects.filter(category_parent__category_url=vendor_url)
    products = Product.objects.filter(product_category__category_url=category_url, product_show=True)
    price_data = ProductVolumePrice.objects.filter(volumeprice_product__product_category__category_url=category_url)
    vendor = ProductVendor.objects.filter(vendor_url=vendor_url)[0]

    content = {
        'products': products,
        'prices': price_data,
        'all_category': all_category,
        'category': category,
        'biofa': False,
        'vendor': vendor
    }
    return render(request,'product/category.html', content)


def vendor_category(request, vendor_url):
    all_category = ProductCategory.objects.filter(category_parent__category_url=vendor_url)
    category = ProductCategory.objects.filter(category_parent__category_url=vendor_url)
    products = Product.objects.filter(product_vendor__vendor_url=vendor_url, product_show=True)
    price_data = ProductVolumePrice.objects.filter(volumeprice_product__product_vendor__vendor_url=vendor_url)
    vendor = ProductVendor.objects.filter(vendor_url=vendor_url)[0]

    content = {
        'category': category,
        'all_category': all_category,
        'products': products,
        'prices': price_data,
        'biofa': False,
        'vendor': vendor
    }
    return render(request,'product/category.html', content)

def all_category(request):
    vendor = ProductVendor.objects.all()

    content = {
        'biofa': False,
        'vendor': vendor
    }
    return render(request, 'product/category.html', content)
