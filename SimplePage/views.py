from django.shortcuts import render

from BiofaImportBD.models import MainpageSimplepage
# from SimplePage.models import SimplePage


def page(request, page_url):
    # selected_page = SimplePage.objects.filter(simple_page_url = page_url)[0]
    selected_page = MainpageSimplepage.objects.using('biofa').filter(simple_page_url = page_url)[0]
    selected_page_2 = MainpageSimplepage.objects.using('biofa').filter(simple_page_url = 'where-could-i-buy')[0]
    context = {
        'page': selected_page,
        'page_2': selected_page_2,
    }
    return render(request, 'simple_page/page.html', context)
