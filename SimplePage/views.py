from django.shortcuts import render

from SimplePage.models import SimplePage


def page(request, page_url):
    """Обычная страница на сайте. Например, контакты, о нас и т.п."""
    selected_page = SimplePage.objects.filter(simple_page_url = page_url)[0]
    context = {
        'page': selected_page,
    }
    return render(request, 'simple_page/page.html', context)
