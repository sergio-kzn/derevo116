from django.shortcuts import render
from BiofaImportBD.models import ProductProduct, ProductVolumepriceproduct, ProductProductProductColor, ProductAttributeproduct


def product(request, category, product):

    biofa_products = ProductProduct.objects.using('biofa').filter(product_category__category_url=category, product_url=product)[0]
    biofa_price_data = ProductVolumepriceproduct.objects.using('biofa').filter(volumeprice_product__product_url=product)
    biofa_colors = ProductProductProductColor.objects.using('biofa').filter(product__product_url=product)
    biofa_attributes = ProductAttributeproduct.objects.using('biofa').filter(attribute_product__product_url=product)
    content = {
        'product': biofa_products,
        'volume_price': biofa_price_data,
        'colors': biofa_colors,
        'attributes': biofa_attributes,
        'biofa': True,
    }
    return render(request, 'product/product.html', content)

def category(request, category):
    return render(request,'product/category.html')
