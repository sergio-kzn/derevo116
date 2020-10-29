from django.shortcuts import render
from BiofaImportBD.models import ProductProduct, ProductVolumepriceproduct, ProductProductProductColor, ProductAttributeproduct, ProductCategoryproduct


def product(request, category_url, product_url):

    biofa_products = ProductProduct.objects.using('biofa').filter(product_url=product_url)[0]
    biofa_price_data = ProductVolumepriceproduct.objects.using('biofa').filter(volumeprice_product__product_url=product_url)
    biofa_colors = ProductProductProductColor.objects.using('biofa').filter(product__product_url=product_url)
    biofa_attributes = ProductAttributeproduct.objects.using('biofa').filter(attribute_product__product_url=product_url)
    content = {
        'product': biofa_products,
        'volume_price': biofa_price_data,
        'colors': biofa_colors,
        'attributes': biofa_attributes,
        'biofa': True,
    }
    return render(request, 'product/product.html', content)


def category(request, category_url):
    biofa_category = ProductCategoryproduct.objects.using('biofa').filter(category_url=category_url)
    biofa_all_category = ProductCategoryproduct.objects.using('biofa').all()
    biofa_products = ProductProduct.objects.using('biofa').filter(product_category__category_url=category_url)
    biofa_price_data = ProductVolumepriceproduct.objects.using('biofa').filter(volumeprice_product__product_category__category_url=category_url)

    content = {
        'products': biofa_products,
        'prices': biofa_price_data,
        'category': biofa_category,
        'all_category': biofa_all_category,
        'biofa': True,
    }
    return render(request, 'product/category.html', content)


def all_category(request):
    biofa_category = ProductCategoryproduct.objects.using('biofa').all()
    biofa_all_category = ProductCategoryproduct.objects.using('biofa').all()
    biofa_products = ProductProduct.objects.using('biofa').all()
    biofa_price_data = ProductVolumepriceproduct.objects.using('biofa').all()

    content = {
        'products': biofa_products,
        'prices': biofa_price_data,
        'category': biofa_category,
        'all_category': biofa_all_category,
        'biofa': True,
    }
    return render(request, 'product/category.html', content)
