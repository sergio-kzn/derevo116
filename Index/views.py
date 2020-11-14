from django.db.models import Q
from django.shortcuts import render

from Product.services import random_from_all_products, last_products
from .models import Slide
from Product.models import Product


def index(request):
    main_slides = Slide.objects.filter(slide_group=1, slide_visible=True)
    slides_2 = Slide.objects.filter(slide_group=2, slide_visible=True)
    banner_1 = Slide.objects.filter(slide_group=3, slide_visible=True)[0]
    slides_3 = Slide.objects.filter(slide_group=4, slide_visible=True)
    banner_2 = Slide.objects.filter(slide_group=5, slide_visible=True)
    banner_3 = Slide.objects.filter(slide_group=6, slide_visible=True)[0]
    brands = Slide.objects.filter(slide_group=7, slide_visible=True)

    random_items = random_from_all_products(4)
    last = last_products(4)

    context = {
        'main_slides': main_slides,
        'slides_2': slides_2,
        'banner_1': banner_1,
        'slides_3': slides_3,
        'banner_2': banner_2,
        'banner_3': banner_3,
        'brands': brands,
        'random_items': random_items,
        'last_items': last,
               }

    biofa_products = Product.objects.filter(product_vendor__vendor_url='biofa')[:5]
    context.update({
        'biofa_products': biofa_products,
    })

    return render(request, 'index/index.html', context)


def search(request):
    items = ""
    if request.GET.__contains__('search'):
        try:
            items = Product.objects.filter(product_show=True)
            q_list = Q()
            for word in request.GET['search'].split():
                q_list |= Q(product_title__icontains=word)
                q_list |= Q(product_extra_desc__icontains=word)
                q_list |= Q(product_vendor_code__icontains=word)
                q_list |= Q(product_content__icontains=word)
                q_list |= Q(product_vendor__vendor_title__icontains=word)
            items = Product.objects.filter(q_list)[:20]
        except:
            pass

    content = {
        'search': request.GET.get('search', default=None),
        'items': items,
    }
    return render(request, 'index/search.html', content)
