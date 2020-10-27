from django.shortcuts import render

from .models import Slide
from BiofaImportBD.models import ProductProduct, ProductVolumepriceproduct
from Product.models import Product, ProductOptionPrice



def index(request):
    main_slides = Slide.objects.filter(slide_group=1, slide_visible=True)
    slides_2 = Slide.objects.filter(slide_group=2, slide_visible=True)
    banner_1 = Slide.objects.filter(slide_group=3, slide_visible=True)[0]
    slides_3 = Slide.objects.filter(slide_group=4, slide_visible=True)
    banner_2 = Slide.objects.filter(slide_group=5, slide_visible=True)
    banner_3 = Slide.objects.filter(slide_group=6, slide_visible=True)[0]
    brands = Slide.objects.filter(slide_group=7, slide_visible=True)
    context = {
        'main_slides': main_slides,
        'slides_2': slides_2,
        'banner_1': banner_1,
        'slides_3': slides_3,
        'banner_2': banner_2,
        'banner_3': banner_3,
        'brands': brands,
               }

    biofa_products = Product.objects.filter(product_vendor__vendor_url='biofa')[:5]
    biofa_price_data = ProductOptionPrice.objects.filter(volumeprice_product__product_vendor__vendor_url='biofa')
    context.update({
        'biofa_products': biofa_products,
        'biofa_prices': biofa_price_data,
    })

    return render(request, 'index/index.html', context)