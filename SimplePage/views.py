import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Product.models import ProductAttribute, ProductCategory, Product, Color, ProductOptionPrice, OptionGroup

from SimplePage.models import SimplePage
from SimplePage.services import update_price


def page(request, page_url):
    """Обычная страница на сайте. Например, контакты, о нас и т.п."""
    selected_page = SimplePage.objects.filter(simple_page_url = page_url)[0]
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
