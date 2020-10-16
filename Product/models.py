from django.db import models


class ProductCategory(models.Model):
    category_parent = models.ForeignKey("self", verbose_name='Родительская категория', null=True, blank=True, on_delete=models.DO_NOTHING)
    category_title = models.CharField(verbose_name='Категория', max_length=100)
    category_sort = models.IntegerField(verbose_name='Сортировка', default=0)
    category_url = models.SlugField(verbose_name='Ссылка url', unique=True)
    category_main_menu = models.BooleanField(verbose_name='Показывать в главном меню?', default=False)
    def __str__(self):
        from django.utils.safestring import mark_safe
        if self.category_parent:
            return mark_safe(f'{self.category_parent.category_title} -- {self.category_title}')
        else:
            return mark_safe(self.category_title)
    class Meta:
        ordering = ['category_parent__id', 'category_sort']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ProductVendor(models.Model):
    """Поставщики товаров"""
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
    def __str__(self):
        return self.vendor_title
    vendor_title = models.CharField(verbose_name='Поставщик', max_length=100)
    vendor_url = models.SlugField(verbose_name='Ссылка url',unique=True)
    vendor_img = models.ImageField(verbose_name='Изображение', upload_to='vendors', blank=True)
    vendor_show = models.BooleanField(verbose_name='Показывать?', default=True)


class ColorGroup(models.Model):
    """объединяет цвета по группам"""
    class Meta:
        verbose_name = "Цвета (группа)"
        verbose_name_plural = "Цвета (группы)"
    def __str__(self):
        return self.color_group_name
    color_group_name = models.CharField(max_length=50)

class Color(models.Model):
    """цвета для масел"""
    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
        ordering = ['color_sort', 'color_title']

    color_title = models.CharField(verbose_name='Цвет', max_length=50)
    color_image = models.ImageField(
        verbose_name='Изображение', upload_to='colors')
    color_sort = models.IntegerField('Сортировка', default=0)
    color_group = models.ForeignKey(ColorGroup, models.DO_NOTHING)

    def __str__(self):
        return self.color_title


class Product(models.Model):
    """товары"""
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['product_title']
    def __str__(self):
        return self.product_title
    product_category = models.ForeignKey(ProductCategory, models.DO_NOTHING, verbose_name='Категория', blank=True, null=True)
    product_vendor = models.ForeignKey(ProductVendor, verbose_name='Поставщик', on_delete=models.DO_NOTHING)
    product_vendor_code = models.CharField(verbose_name='Артикул', unique=True, max_length=20)
    product_title = models.CharField(verbose_name='Заголовок', max_length=200)
    product_img = models.ImageField(verbose_name='Изображение товара',upload_to=f'products/{ProductCategory.category_url}/')
    product_description = models.TextField(verbose_name='Дополнительное описание товара', blank=True, null=True)
    product_content = models.TextField(verbose_name='Описание', )
    product_url = models.SlugField(verbose_name='Ссылка url', unique=True, max_length=100)
    product_file = models.FileField(verbose_name='Прикрепить файл (Техническое руководство) pdf', upload_to='product/files', null=True, blank=True)
    product_count = models.CharField(verbose_name='Наличие товара', max_length=30, blank=True, null=True, default="В наличии более 10л.")
    product_show = models.BooleanField(verbose_name='Показывать?', default=True)
    product_color = models.ManyToManyField(ColorGroup, verbose_name="Группа цветов", blank=True)
    product_price = models.CharField(verbose_name='Цена (если пусто, то цена берется из таблицы ниже)', max_length=30, blank=True, null=True)
    product_price_title = models.CharField(verbose_name='Название опции для нескольких цен', max_length=30, blank=True, null=True, default="Объем")



class ProductAttribute(models.Model):
    """атрибуты для товаров
    показываются в отдельной вкладке"""
    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"
        ordering = ['attribute_sort', 'attribute_title']
    def __str__(self):
        if self.attribute_title == None:
            return f'(id={self.id})'
        return str(self.attribute_title)
    attribute_title = models.CharField(max_length=200, verbose_name='Атрибут', blank=True, null=True)
    attribute_value = models.CharField(max_length=200, verbose_name='Значение атрибута (необязательно)', blank=True, null=True)
    attribute_sort = models.IntegerField(verbose_name='Сортировка', default=0)
    attribute_product = models.ForeignKey(Product, models.DO_NOTHING, verbose_name='Товар')


class ProductColor(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING)
    color = models.ForeignKey(Color, models.DO_NOTHING)


class Volume(models.Model):
    """опции, используются для товаров, у которых несколько опций цен"""
    class Meta:
        verbose_name = "Опция"
        verbose_name_plural = "Опции"
        ordering = ['volume_sort', 'volume_title']
    def __str__(self):
        return self.volume_title
    volume_title = models.CharField(verbose_name='Опция', max_length=10)
    volume_sort = models.IntegerField(verbose_name='Сортировка', default=0)


class ProductVolumePrice(models.Model):
    """таблица для товаров, у которых несколько опций цен"""
    class Meta:
        verbose_name = "Опция"
        verbose_name_plural = "Опции"
        ordering = ['volumeprice_sort', 'volumeprice_volume']

    volumeprice_volume = models.ForeignKey(Volume, models.DO_NOTHING, verbose_name='Опции')
    volumeprice_price = models.CharField(max_length=10, verbose_name='Цены')
    volumeprice_sort = models.IntegerField(verbose_name='Сортировка', default=0)
    volumeprice_product = models.ForeignKey(Product, models.DO_NOTHING, verbose_name='Товар')
