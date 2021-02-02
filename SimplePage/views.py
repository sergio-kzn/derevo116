from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Product.models import ProductAttribute, ProductCategory, Product

from SimplePage.models import SimplePage


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
