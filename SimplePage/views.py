import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Product.models import ProductAttribute, ProductCategory, Product, Color
from Product.services import last_products

from SimplePage.models import SimplePage
from SimplePage.services import update_price, parcer_cosca_product, create_new_item


def page(request, page_url):
    """Обычная страница на сайте. Например, контакты, о нас и т.п."""
    selected_page = SimplePage.objects.filter(simple_page_url=page_url)[0]
    context = {
        'page': selected_page,
    }
    return render(request, 'simple_page/page.html', context)


@login_required(login_url='/admin/login/')
def find_attr(request):
    attr = dict()
    for category in ProductCategory.objects.all():
        attributes = set()
        for attribute in ProductAttribute.objects.filter(attribute_product__product_category=category).exclude(attribute_title=None):
            attributes.add(str(attribute))
        if len(attributes) > 0:
            attr[category] = attributes

    context = {
        'attr': attr,
    }
    return render(request, 'simple_page/find_attr.html', context)


@login_required(login_url='/admin/login/')
@csrf_exempt
def price_list_biofa(request):
    if request.method == 'POST':
        new_price = json.loads(request.body)
        if update_price(new_price):
            return HttpResponse('OK')
    else:
        categories = ProductCategory.objects.filter(category_parent=54)
        biofa = Product.objects.filter(product_category__category_parent=54)
        colors = Color.objects.filter(color_group__product__product_category__category_parent=54)

        context = {
            "categories": categories,
            "products": biofa,
            "colors": colors,
        }
        return render(request, 'simple_page/price_list_biofa.html', context)


@login_required(login_url='/admin/login/')
def scraping_cosca(request):
    if request.method == 'POST':
        if json.loads(request.body).get('url'):
            url = json.loads(request.body)['url']
            return JsonResponse(parcer_cosca_product(url))
        elif json.loads(request.body).get('new_item'):
            data = json.loads(request.body)['new_item']
            return create_new_item(data)
        else:
            return HttpResponse(500)

    return render(request, 'simple_page/cosca.html', {'last_items': Product.objects.filter(product_show=True).filter(product_vendor_id=11).order_by('-id')[:1]
})

@login_required(login_url='/admin/login/')
def images_to_gallery(request):
    if request.method == 'POST':
        images_raw = json.loads(request.body)['images']
        print(images_raw)

        return HttpResponse('Получено')

    return render(request, 'simple_page/images_to_gallery.html', {})
