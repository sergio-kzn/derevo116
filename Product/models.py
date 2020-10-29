from django.db import models
from sorl.thumbnail import ImageField



class ProductCategory(models.Model):
    category_parent = models.ForeignKey("self", verbose_name='Родительская категория', null=True, blank=True, on_delete=models.DO_NOTHING)
    category_title = models.CharField(verbose_name='Категория', max_length=100)
    category_sort = models.IntegerField(verbose_name='Сортировка', default=0)
    category_url = models.SlugField(verbose_name='Ссылка url (проверьте vendor_url)', unique=True)
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
        ordering = ['vendor_sort']
    def __str__(self):
        return self.vendor_title
    vendor_title = models.CharField(verbose_name='Поставщик', max_length=100)
    vendor_url = models.SlugField(verbose_name='Ссылка url',unique=True)
    vendor_img = ImageField(verbose_name='Изображение', upload_to='vendors', blank=True)
    vendor_sort = models.IntegerField(verbose_name='Сортировка', default=0)
    vendor_show = models.BooleanField(verbose_name='Показывать?', default=True)


class ColorGroup(models.Model):
    """объединяет цвета по группам"""
    class Meta:
        verbose_name = "Цвета (группа)"
        verbose_name_plural = "Цвета (группы)"
    def __str__(self):
        return self.color_group_name
    color_group_name = models.CharField(verbose_name='Группа цветов', max_length=100)

class Color(models.Model):
    """цвета для масел"""
    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
        ordering = ['color_sort', 'color_title']
    def __str__(self):
        return self.color_title
    color_title = models.CharField(verbose_name='Название цвета', max_length=50)
    color_image = ImageField(verbose_name='Изображение', upload_to='products/colors')
    color_sort = models.IntegerField('Сортировка', default=0)
    color_group = models.ForeignKey(ColorGroup, models.DO_NOTHING)


class ProductTab(models.Model):
    """Дополнительные вкладки на странице товара"""
    class Meta:
        verbose_name = "Вкладка"
        verbose_name_plural = "Вкладки"
    def __str__(self):
        return str(self.tab_title_admin)

    tab_title_admin = models.CharField(verbose_name='Название (в админке)', max_length=200)
    tab_title = models.CharField(verbose_name='Название (в шаблоне)', max_length=200)
    tab_content = models.TextField(verbose_name='Содержимое доп. вкладки', blank=True, null=True)
    tab_slug = models.SlugField(verbose_name='Ссылка href="# ..."', default='additionally')


class OptionGroup(models.Model):
    TYPES = [
        ('1', 'Radio Inputs'),
        ('2', 'Buttons'),
    ]
    option_group = models.CharField(verbose_name='Название группы опций', max_length=100, help_text='Например, название товара, к которому эти опции относятся')
    option_type = models.CharField(verbose_name='Тип опций', max_length=50, choices=TYPES, default='1')
    option_title = models.CharField(verbose_name='Заголовок', max_length=100, blank=True, null=True, help_text='Отображается рядом с опциями на странице товара')
    product_price_option = models.CharField(verbose_name='Опция', max_length=50, blank=True, null=True, default="Объем")
    product_price_option_price = models.CharField(verbose_name='Цена', max_length=50, blank=True, null=True, default="Цена")
    product_price_option_extra_1 = models.CharField(verbose_name='Дополнительно 1', max_length=50, blank=True, null=True, help_text="Расход&nbsp;м&lt;sup&gt;2&lt;/sup&gt;&lt;br&gt;(1&nbsp;слой&nbsp;/&nbsp;2&nbsp;слоя)<br>")
    product_price_option_extra_2 = models.CharField(verbose_name='Дополнительно 2', max_length=50, blank=True, null=True, help_text="Цена&nbsp;р/м&lt;sup&gt;2&lt;/sup&gt;&lt;br&gt;(1&nbsp;слой&nbsp;/&nbsp;2&nbsp;слоя)")
    def __str__(self):
        return self.option_group
    class Meta:
        verbose_name = "Опция (группа)"
        verbose_name_plural = "Опции (группы)"


class ProductImageGroup(models.Model):
    img_group = models.CharField(verbose_name='Дополнительные изображения', max_length=100, help_text='Название группы изображений, например название Товара')

    def __str__(self):
        return self.img_group

    class Meta:
        verbose_name = 'Изображение (группа)'
        verbose_name_plural = 'Изображения (группы)'


class ProductImage(models.Model):
    img_file = ImageField(verbose_name='Изображение товара', upload_to='products')
    img_title = models.CharField(verbose_name='Подпись', max_length=100)
    img_group = models.ForeignKey(ProductImageGroup, models.DO_NOTHING)


class Product(models.Model):
    """товары"""
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    def __str__(self):
        return self.product_title
    PRICE = [
        ('1', 'Простая цена'),
        ('2', 'Цена с опциями'),
    ]
    product_show = models.BooleanField(verbose_name='Показывать?', default=True)
    product_category = models.ForeignKey(ProductCategory, models.DO_NOTHING, verbose_name='Категория', blank=True, null=True)
    product_vendor = models.ForeignKey(ProductVendor, verbose_name='Поставщик', on_delete=models.DO_NOTHING)
    product_vendor_code = models.CharField(verbose_name='Артикул', unique=True, max_length=20)
    product_title = models.CharField(verbose_name='Заголовок', max_length=200)
    product_url = models.SlugField(verbose_name='Ссылка url', unique=True, max_length=100)
    product_extra_desc = models.TextField(verbose_name='Краткое описание', blank=True, null=True, help_text='Дополнительная информация, показывается рядом с ценой')
    product_img = ImageField(verbose_name='Изображение товара',upload_to='products', blank=True, null=True, help_text='Основное изображение товара, рекомендуемый размер 1000х700 px')
    product_img_title = models.CharField(verbose_name='Подпись', max_length=100, blank=True, null=True, help_text='Подпись под изображением и alt')
    product_images = models.ManyToManyField(ProductImageGroup, verbose_name='Дополнительные изображения товара', blank=True)
    # product_description_title = models.CharField(verbose_name='Название доп. вкладки', max_length=200, blank=True, null=True)
    # product_description = models.TextField(verbose_name='Содержимое доп. вкладки', blank=True, null=True)
    product_content = models.TextField(verbose_name='Описание', blank=True, null=True)
    product_file = models.FileField(verbose_name='Прикрепить файл (Техническое руководство) pdf', upload_to='product/files', null=True, blank=True)
    product_count = models.CharField(verbose_name='Наличие товара', max_length=30, blank=True, null=True, default="В наличии более 10л.")
    product_color = models.ManyToManyField(ColorGroup, verbose_name="Группа цветов", blank=True)
    product_tab = models.ManyToManyField(ProductTab, verbose_name="Доп. вкладки", blank=True)
    product_price_choice = models.CharField(verbose_name='Тип цены', choices=PRICE, default='2', max_length=50)
    product_price = models.CharField(verbose_name='Простая цена (Руб.)', max_length=30, blank=True, null=True, help_text='Введите цену без копеек и без знака рубля')
    product_price_options = models.ManyToManyField(OptionGroup, verbose_name='Опции цены', blank=True)


class ProductAttribute(models.Model):
    """атрибуты для товаров
    показываются в отдельной вкладке"""
    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"
        ordering = ['attribute_sort', 'id']
    def __str__(self):
        if self.attribute_title == None:
            return f'(id={self.id})'
        return str(self.attribute_title)
    attribute_distinguish_bold = models.BooleanField(verbose_name="<b>", default=False, help_text='Выделяет всю строку жирным')
    attribute_distinguish_yellow = models.BooleanField(verbose_name="bg-y", default=False, help_text='Выделяет всю строку желтым фоном')
    attribute_distinguish_empty = models.BooleanField(verbose_name="nbsp", default=False, help_text='Включите, если хотите добавить пустую строку')
    attribute_distinguish_colspan = models.BooleanField(verbose_name="2:1", default=False, help_text='Объединяет ячейки в одну')
    attribute_title = models.CharField(max_length=200, verbose_name='Атрибут', blank=True, null=True)
    attribute_value = models.CharField(max_length=200, verbose_name='Значение атрибута (необязательно)', blank=True, null=True,)
    attribute_sort = models.IntegerField(verbose_name='Сортировка', default=0)
    attribute_product = models.ForeignKey(Product, models.DO_NOTHING, verbose_name='Товар')


class OptionPrice(models.Model):
    """Список опций"""
    class Meta:
        verbose_name = "Опция"
        verbose_name_plural = "Опции"
        ordering = ['option_sort', 'option_title']
    def __str__(self):
        return self.option_title
    option_title = models.CharField(verbose_name='Опция', max_length=20)
    option_sort = models.IntegerField(verbose_name='Сортировка', default=0)


class ProductOptionPrice(models.Model):
    """опция - цена - дополнительно - ..."""
    class Meta:
        verbose_name = "Опция"
        verbose_name_plural = "Опции"
        ordering = ['product_option_sort', 'product_option']

    product_option_group = models.ForeignKey(OptionGroup, models.DO_NOTHING, verbose_name='Группа опций')
    product_option = models.ForeignKey(OptionPrice, models.DO_NOTHING, verbose_name='Выберите опцию')
    product_option_price = models.CharField(max_length=10, verbose_name='Цена')
    product_option_extra_1 = models.CharField(max_length=50, verbose_name='Дополнительно 1', blank=True, null=True)
    product_option_extra_2 = models.CharField(max_length=50, verbose_name='Дополнительно 2', blank=True, null=True)
    product_option_sort = models.IntegerField(verbose_name='Сортировка', default=0)
