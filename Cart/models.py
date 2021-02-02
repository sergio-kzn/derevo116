from django.db import models

from Product.models import Product, Color


class Country(models.Model):
    """Страны для доставки"""
    country_name = models.CharField(verbose_name='Страна', max_length=100)
    country_default = models.BooleanField('По умолчанию', default=False)
    country_order = models.IntegerField('Сортировка', default=0)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['country_order']

    def __str__(self):
        return self.country_name


class City(models.Model):
    """Город для доставки"""
    city_name = models.CharField(verbose_name='Город', max_length=100)
    city_country = models.ForeignKey(verbose_name='Страна', to=Country, on_delete=models.CASCADE)
    city_default = models.BooleanField('По умолчанию', default=False)
    city_order = models.IntegerField('Сортировка', default=0)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['city_order']

    def __str__(self):
        return self.city_name


class Delivery(models.Model):
    """Варианты доставки"""
    delivery_API = models.IntegerField('API номер', unique=True)
    delivery_title = models.CharField(verbose_name='Название', max_length=100)
    delivery_description = models.TextField(verbose_name='Описание')
    delivery_img = models.ImageField(verbose_name='Изображение', upload_to='delivery', null=True, blank=True)
    delivery_enable = models.BooleanField(verbose_name='Включить', default=True)
    delivery_city = models.ManyToManyField(City, verbose_name='Города для доставки', blank=True)
    delivery_pickup = models.BooleanField('Самовывоз', default=0)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Варианты доставки'

    def __str__(self):
        return self.delivery_title


class Payment(models.Model):
    """Варианты оплаты"""
    payment_API = models.IntegerField('API номер', unique=True)
    payment_title = models.CharField(verbose_name='Название', max_length=100)
    payment_description = models.TextField(verbose_name='Описание', null=True, blank=True)
    payment_enable = models.BooleanField(verbose_name='Включить', default=True)
    payment_delivery = models.ManyToManyField(Delivery, verbose_name='Доставка', blank=True)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Варианты оплаты'

    def __str__(self):
        return self.payment_title


class Status(models.Model):
    """Статус заказа"""
    status_name = models.CharField(verbose_name='Статус', max_length=100)
    status_order = models.IntegerField(verbose_name='Сортировка', default=0)
    status_default = models.BooleanField(verbose_name='По умолчанию', default=0)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'
        ordering = ['status_order']

    def __str__(self):
        return self.status_name


class Order(models.Model):
    """Собственно сам заказ"""
    order_number = models.CharField(verbose_name='Номер заказа', unique=True, max_length=20)
    order_delivery = models.ForeignKey(Delivery, models.DO_NOTHING, verbose_name='Доставка')
    order_delivery_other = models.TextField(verbose_name='Своя доставка', null=True, blank=True)
    order_payment = models.ForeignKey(Payment, models.DO_NOTHING, verbose_name='Оплата')
    order_status = models.ForeignKey(Status, models.DO_NOTHING, verbose_name='Статус заказа')
    order_history = models.TextField(verbose_name='История заказа', null=True, blank=True)
    order_comment = models.TextField(verbose_name='Комментарий от клиента', null=True, blank=True)
    order_comment_admin = models.TextField(verbose_name='Комментарий администратора', help_text='Клиент этого не видит', null=True, blank=True)
    order_country_city_index = models.CharField(max_length=255, verbose_name='Страна, город, индекс', null=True, blank=True)
    order_address = models.CharField(max_length=255, verbose_name='Улица, дом, квартира', null=True, blank=True)
    order_client_name = models.CharField(max_length=255, verbose_name='Имя клиента', null=True, blank=True)
    order_phone = models.CharField(max_length=255, verbose_name='Номер телефона', null=True, blank=True)
    order_notification = models.BooleanField(verbose_name='Уведомлять по email?', default=0)
    order_email = models.EmailField(verbose_name='Email для уведомлений', null=True, blank=True)
    order_call_me = models.BooleanField(verbose_name='Позвонить для подтверждения?', default=1)
    order_sum = models.IntegerField(verbose_name='Сумма заказа', default=0)

    class Meta:
        verbose_name = 'ЗАКАЗ'
        verbose_name_plural = 'ЗАКАЗЫ'

    def __str__(self):
        return self.order_number


class Item(models.Model):
    """Товар с выбранными опциями, который добавлется в заказ"""
    item_product = models.ForeignKey(Product, verbose_name="Товар из БД", on_delete=models.DO_NOTHING)
    item_id = models.CharField(verbose_name="ID", max_length=255)
    item_color = models.CharField(verbose_name="Цвет", max_length=255, null=True, blank=True)
    item_options = models.CharField(verbose_name="Опции", max_length=255, null=True, blank=True)
    item_price = models.IntegerField(verbose_name='Цена', default=0)
    item_count = models.IntegerField(verbose_name='Кол-во', default=0)
    item_sale = models.IntegerField(verbose_name='Скидка %', default=0)
    item_sum = models.IntegerField(verbose_name='Сумма', default=0)
    item_order = models.ForeignKey(Order, to_field='order_number', on_delete=models.CASCADE, verbose_name='Заказ', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    def __str__(self):
        return self.item_id
