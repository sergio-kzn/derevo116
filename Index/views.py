import csv
import re

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from sorl.thumbnail import get_thumbnail

from Product.services import random_from_all_products, last_products
from .models import Slide
from Product.models import Product, OptionGroup, ProductOptionPrice, ProductCategory


def index(request):
    """Главная домащняя страница"""
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
    """Страница поиска товаров"""
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


def yandex(request):
    """страница проверки прав в яндекс.вебмастер"""
    return render(request, 'yandex_545a557cc12bb32d.html')


def facebook_export_product_in_csv(request):
    """
    https://www.facebook.com/business/help/1898524300466211?id=725943027795860
    Поле	        Описание
    id              Максимально допустимое количество символов: 100.
                    Пример: 12345
    title           Максимально допустимое количество символов: 150.
                    Пример: "Синяя хлопковая футболка"
    description     Укажите особые характеристики товара, такие как материал или цвет.
                    Используйте обычный текст (без HTML-кода), не пишите заглавными буквами и не добавляйте ссылки.
                    Максимально допустимое количество символов: 5 000.
                    Пример: "Женская футболка из органического хлопка в глубоком синем цвете. Свободная посадка"
    availability    Текущая доступность товара. Поддерживаемые значения:
                    - in stock (в наличии),
                    - available for order (доступно для заказа),
                    - out of stock (нет в наличии).
                    Если товара нет в наличии, то в каналах продаж он получит соответствующую метку и вообще не будет появляться в объявлениях.
                    Пример: in stock
    condition       Состояние товара. Поддерживаемые значения:
                    - new (новый),
                    - refurbished (после ремонта),
                    - used (б/у).
                    Пример: new
    price           Цена товара. Укажите цену в виде числа с трехбуквенным кодом валюты согласно стандарту ISO через пробел.
                    Используйте в качестве десятичного разделителя точку ("."), а не запятую (",").
                    Не вводите символы валюты, например "$".
                    Используйте одну валюту на каталог, чтобы цены товаров были единообразными.
                    Примеры: 9.99 USD или 7.99 EUR
    link            URL страницы сайта, где можно узнать больше о товаре или купить его.
                    Ссылки должны быть рабочими и начинаться с http:// или https://.
                    Пример: http://www.jaspersmarket.com/products/shirt
    image_link      URL основного изображения товара. Изображения должны быть в форматах JPG, GIF или PNG,
                    иметь разрешение как минимум 500 x 500 пикселей и размер до 8 МБ.
                    Пример: http://www.jaspersmarket.com/products/shirt.jpg
                    Примечание. Если в дальнейшем вы замените изображение, его URL должен отличаться от текущего.
                    Иначе изменения не будут распознаны.
    brand           Название бренда, коды MPN или GTIN для товара.
                    Указать нужно не все эти варианты, а только один из них.
                    В качестве GTIN укажите UPC, EAN, JAN или ISBN товара.
                    Максимально допустимое количество символов: 100.
                    Пример: Jasper's Market
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="facebook_products.csv"'

    writer = csv.writer(response, delimiter=";")
    writer.writerow(['id', 'title', 'description', 'availability', 'condition', 'price', 'link', 'image_link', 'brand'])

    products = Product.objects.filter(product_show=True)
    for product in products:
        id = product.product_vendor_code
        title = product.product_title[:100]
        description = re.sub(r'\<[^>]*\>', ' ', product.product_extra_desc)
        description = re.sub(r';', ',', description)
        description = re.sub(r'&nbsp;', ' ', description)
        if 'в наличии' in product.product_count.lower():
            availability = 'in stock'
        elif 'под заказ' in product.product_count.lower():
            availability = 'available for order'
        else:
            availability = 'out of stock'
        condition = 'new'

        if product.product_price_choice == "1":
            price = product.product_price.replace(" ", "").strip()
        elif product.product_price_choice == "2":
            groups = OptionGroup.objects.filter(product__product_url=product.product_url).order_by('options_sort')
            price = 999999999
            for group in groups:
                prices = ProductOptionPrice.objects.filter(product_option_group=group).order_by('product_option_price')
                try:
                    min_price = prices.first().product_option_price.replace(" ", "").strip()
                    if int(price) > int(min_price):
                        price = min_price
                except AttributeError:
                    pass
        else:
            price = 0
        price = f'{price} RUB'

        url_product = product.product_url
        url_category = ProductCategory.objects.get(category_url=product.product_category.category_url).category_url
        url_vendor = ProductCategory.objects.get(category_url=product.product_category.category_parent.category_url).category_url
        url_root_category = ProductCategory.objects.get(category_url=product.product_category.category_parent.category_parent.category_url).category_url
        # url_host = request.headers['Host']
        url_host = 'https://derevo116.ru'
        link = f'{url_host}//{url_root_category}/{url_vendor}/{url_category}/{url_product}/'

        im = get_thumbnail(product.product_img, '650x650', padding=True, format="WEBP")
        image_link = f'{url_host}/{im.url}'

        brand = product.product_vendor.vendor_title

        writer.writerow([id, title, description, availability, condition, price, link, image_link, brand])
    return response
    # return HttpResponse()
