from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse

from Product.models import ProductOptionPrice as Price, ProductCategory, Product, ProductVendor, OptionGroup, \
    ProductOptionPrice, OptionPrice, ProductAttribute, ProductTab
from loguru import logger


def update_price(dict):
    # {'306': {'new_price': '539', 'new_price_rate': '216  /  359'},
    #  '307': {'new_price': '1 507', 'new_price_rate': '201  /  343'},
    #  '308': {'new_price': '3 740', 'new_price_rate': '187  /  288'},
    #  '309': {'new_price': '8 872', 'new_price_rate': '177  /  277'}}
    logger.add("file_1.log", rotation="500 MB", format="{time} {level} {message}")
    for id in dict:
        price = Price.objects.get(id=id)

        logger.info('id={} | old price={}', price.id, price.product_option_price)
        logger.info('id={} | old price_rate={}', price.id, price.product_option_extra_2)

        price.product_option_price = dict[id]['new_price']

        if dict[id]['new_price_rate'] == 'None':
            price.product_option_extra_2 = None
        else:
            price.product_option_extra_2 = dict[id]['new_price_rate']

        price.save()

        logger.info('id={} | new price={}', price.id, price.product_option_price)
        logger.info('id={} | new price_rate={}', price.id, price.product_option_extra_2)

    return True


def parcer_cosca_product(url: str) -> dict:
    """
    парсим страницу с товаром
    url: example: https://cosca.ru/internet-magazin/product/naturalnyye-oboi-cosca-arabesko-disko-0-91-x-10-m
    """
    context = {}
    soup = BeautifulSoup(urlopen(url), features="lxml")
    try:
        category = ProductCategory.objects.get(category_title=soup.find('div', class_="site-path").contents[4].string)
        context['category'] = category.category_title
        context['category_id'] = category.id
    except IndexError:
        print(soup.find('div', class_="site-path").contents)
    context['vendor'] = 11  # cosca decolingi
    context['vendor_code'] = soup.find('div', class_="shop2-product-article").get_text().split(": ")[1]
    try:
        context['title'] = soup.find('div', class_="site-path").contents[5].string.replace("/", "").strip().split(",")[0]
    except IndexError:
        print(soup.find('div', class_="site-path").contents)
    table = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'j', 'з': 'z', 'и': 'i',
             'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
             'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'u', 'я': 'ya'}
    new_url = context['vendor_code'].lower()
    for key in table:
        new_url = new_url.replace(key, table[key])
    context['url'] = f"{new_url}-cosca-decolingi"

    context['count'] = 'Под заказ'
    context[
        # 'short_description'] = 'Материал наклеен на основу из неотбеленной бумаги. Натуральные обои дарят эстетическое наслаждение и энергетику природы. Экологически чистые,  прочные и плотные, скрывают неровности стены, обладают  высокой тепло- и звукоизоляцией, просты в уходе.  Цена указана за рулон.'
        'short_description'] = 'Натуральные обои дарят эстетическое наслаждение и энергетику природы. Цена указана за рулон.'
    attrs = {}
    for attr in soup.find('table', class_='shop2-product-options').contents:
        if attr.find('th').get_text() == 'Материал обоев':
            attrs['Материал обоев'] = attr.find('td').get_text()[0].upper() + attr.find('td').get_text()[1:]
        if attr.find('th').get_text() == 'Ширина':
            attrs['Ширина'] = attr.find('td').get_text()
        if attr.find('th').get_text() == 'Тип рисунка':
            attrs['Тип рисунка'] = attr.find('td').get_text()[0].upper() + attr.find('td').get_text()[1:]
        if attr.find('th').get_text() == 'Цвет обоев':
            attrs['Цвет обоев'] = attr.find('td').get_text(strip=True)[0].upper() + attr.find('td').get_text(
                strip=True)[1:]
        if attr.find('th').get_text() == 'Длина рулона':
            attrs['Длина рулона'] = attr.find('td').get_text()
        if attr.find('th').get_text() == 'Коллекция обоев':
            attrs['Коллекция обоев'] = attr.find('td').get_text()[0].upper() + attr.find('td').get_text()[1:]
        if attr.find('th').get_text() == 'Страна производства':
            attrs['Страна производства'] = attr.find('td').get_text()[0].upper() + attr.find('td').get_text()[1:]
    context['attr'] = attrs
    context['attr_count'] = len(attrs)
    context['img'] = 'https://' + url.split('/')[2] + soup.find(itemprop="image")['src']
    if soup.find('div', class_="product-thumbnails"):
        context['other_img'] = "Есть"
    else:
        context['other_img'] = "Нет"

    context['price'] = soup.find('div', class_="price-current").contents[1].get_text()

    return context

def create_new_item(data: dict) -> JsonResponse:
    """Добавляет Продукт в БД"""
    try:
        new_item = Product.objects.get(product_vendor_code=data['vendor_code'])
        print('Обновление продукта... id=' + str(new_item.id))
    except ObjectDoesNotExist:
        new_item = Product()
        print('Создание нового продукта...')
    new_item.product_category = ProductCategory.objects.get(category_title=data['category'])
    new_item.product_vendor = ProductVendor.objects.get(id=11)
    new_item.product_vendor_code = data['vendor_code']
    new_item.product_title = data['title']
    new_item.product_url = data['url']
    new_item.product_extra_desc = data['short_description']
    new_item.product_count = data['count']
    new_item.product_img_title = data['title'].split(',')[0]
    if data['price_type'] == 1:
        print('Простая цена')
        new_item.product_price_choice = data['price_type']
        new_item.product_price = data['price']
    elif data['price_type'] == 2:
        print('Цена с опциями')
        new_item.product_price_choice = data['price_type']
        new_item.product_price = 0
        try:
            new_option_group = OptionGroup.objects.get(option_group=data['title'].split(',')[0])
            print('Редактируем группу опций id=' + str(new_option_group.id))
        except ObjectDoesNotExist:
            new_option_group = OptionGroup()
            print('Создаем новую группу опций...')
            new_option_group.option_group = data['title'].split(',')[0]
            new_option_group.product_price_option = 'Длина рулона'
            new_option_group.save()
        print('Группа опций готова')

        # print(data['price_options'])
        print('Созадем опции')
        print('\t5.5 м', end=' ')
        try:
            new_option_price_5 = ProductOptionPrice.objects.filter(product_option_group=new_option_group).get(
                product_option=OptionPrice.objects.get(id=49))
            print('- Редактируем опцию id=' + str(new_option_price_5.id))
        except ObjectDoesNotExist:
            print('- Создаем новую опцию')
            new_option_price_5 = ProductOptionPrice()
            new_option_price_5.product_option_group = new_option_group
            new_option_price_5.product_option = OptionPrice.objects.get(id=49)
        new_option_price_5.product_option_price = data['price_options']['5']
        new_option_price_5.save()
        print('\t5.5 м - СОХРАНЕНО')

        print('\t10 м', end=' ')
        try:
            new_option_price_10 = ProductOptionPrice.objects.filter(product_option_group=new_option_group).get(
                product_option=OptionPrice.objects.get(id=48))
            print('- Редактируем опцию id=' + str(new_option_price_10.id))
        except ObjectDoesNotExist:
            print('- Создаем новую опцию')
            new_option_price_10 = ProductOptionPrice()
            new_option_price_10.product_option_group = new_option_group
            new_option_price_10.product_option = OptionPrice.objects.get(id=48)
        new_option_price_10.product_option_price = data['price_options']['10']
        new_option_price_10.save()
        print('\t10 м - СОХРАНЕНО')

    # img
    # FIXME: Добавить проверку что такое изображение уже есть
    # if data['img'].split('/')[-1] in ...
    # print('Такое изображение уже есть')
    # ИЗВИНИТЕ за следующий код. я не пониманию все эти преобразования, я просто скопировал это из интернета.
    print('Загружаем Изображение', end='\r')
    from PIL import Image
    import requests
    response = requests.get(data['img'], stream=True)
    response.raw.decode_content = True
    img = Image.open(response.raw)
    from io import BytesIO
    from django.core.files import File
    blob = BytesIO()
    format = 'JPEG'
    # if data['img'].split('.')[-1].lower() == 'jpg':
    #     format = 'JPEG'
    img.save(blob, format)
    new_item.product_img.save(data['img'].split('/')[-1], File(blob), save=False)
    print('Изображение загружено')

    attrs = dict(data['attrs'])
    product_tab = ProductTab.objects.get(id=22)  #Cosca Обои Преимущества
    new_tabs = []
    for attr_title, attr_value in attrs.items():
        if 'материал' in attr_title.lower():
            if 'бамбук' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=23))
            if 'джут' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=24))
            if 'тростник' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=25))
            if 'сизал' in attr_value.lower() and 'бархат' not in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=26))
            if 'златоцвет' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=27))
            if 'сизал' in attr_value.lower() and 'бархат' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=28))
            if 'ситник' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=29))
            if 'крапив' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=30))
            if 'лен' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=31))
            if 'магноли' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=32))
            if 'вьюн' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=33))
            if 'будд' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=34))
            if 'слюда' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=35))
            if 'шпон' in attr_value.lower() and 'пробк' in attr_value.lower() and 'дуб' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=36))
            if 'шпон' in attr_value.lower() and 'абак' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=37))
            if 'шпон' in attr_value.lower() and 'шанхай' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=38))
            if 'велюр' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=39))
            if 'хлоп' in attr_value.lower() and 'ткань' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=40))
            if 'цел' in attr_value.lower() and 'волокно' in attr_value.lower() and 'тканая' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=41))
            if 'бумага' in attr_value.lower() and 'нетканая' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=42))
            if 'папирус' in attr_value.lower():
                new_tabs.append(ProductTab.objects.get(id=43))
    print(f'Вкладки: {new_tabs}')

    print('Данные обработаны')
    try:
        print('Проверка...', end='\r')
        new_item.full_clean()
        print('Проверка прошла успешно')
        print('Сохраняем...', end='\r')
        new_item.save()
        print('СОХРАНЕНО')

        #     атрибуты
        print('Созадем атрибуты')
        for attr_title, attr_value in attrs.items():
            try:
                new_attr = ProductAttribute.objects.filter(attribute_product_id=new_item.id).get(attribute_title=attr_title)
                print('\tРедактируем атрибут id=' + str(new_attr.id))
            except ObjectDoesNotExist:
                print('\tСоздаем новый атрибут')
                new_attr = ProductAttribute()
                new_attr.attribute_product = new_item
                new_attr.attribute_title = attr_title
            new_attr.attribute_value = attr_value
            new_attr.save()
            # print('\tАтрибут - СОХРАНЕН')

        new_item.product_tab.add(product_tab)
        for tab in new_tabs:
        # if len(new_tabs) > 0:
            new_item.product_tab.add(tab)

        if data['price_type'] == 2:
            new_item.product_price_options.add(new_option_group)

        return JsonResponse(
            data={'id': new_item.id, 'url': new_item.product_category.category_url + '/' + new_item.product_url + '/'},
            status=200)

    except ValidationError as e:
        print('Проверка провалилась!')
        return JsonResponse(e.message_dict, safe=False, status=500)
