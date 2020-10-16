from django.shortcuts import render

from Product.models import Product, ProductVolumePrice, ProductColor, ProductAttribute


def product(request, vendor_url, category_url, product_url):
    product = Product.objects.filter(product_url=product_url)[0]
    price_data = ProductVolumePrice.objects.filter(volumeprice_product__product_url=product_url)
    colors = ProductColor.objects.filter(product__product_url=product_url)
    attributes = ProductAttribute.objects.filter(attribute_product__product_url=product_url)
    content = {
        'product': product,
        'volume_price': price_data,
        'colors': colors,
        'attributes': attributes,
        'biofa': False,
    }
    return render(request, 'product/product.html', content)


def category(request, vendor, category):
    return render(request,'product/category.html')

def vendor_category(request, vendor):
    return render(request,'product/category.html')

def all_category(request):
    return render(request,'product/category.html')
