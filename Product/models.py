from django.db import models


class ProductCategory(models.Model):
    category_title = models.CharField(max_length=100)
    category_sort = models.IntegerField()
    category_url = models.CharField(unique=True, max_length=100)


class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory, models.DO_NOTHING, blank=True, null=True)
    product_vendor = models.CharField(max_length=100) # FIXME: переделать на связь с отдельным класом
    product_title = models.CharField(max_length=60)
    product_vendor_code = models.CharField(unique=True, max_length=10)
    product_img = models.CharField(max_length=100)
    product_description = models.TextField(blank=True, null=True)
    product_content = models.TextField()
    product_url = models.CharField(unique=True, max_length=50)
    product_file = models.CharField(max_length=100, blank=True, null=True)
    product_price = models.CharField(max_length=30, blank=True, null=True)
    product_count = models.CharField(max_length=30, blank=True, null=True)


class ProductAttribute(models.Model):
    attribute_title = models.CharField(max_length=200)
    attribute_sort = models.IntegerField()
    attribute_product = models.ForeignKey(Product, models.DO_NOTHING)


class ColorGroup(models.Model):
    color_group_name = models.CharField(max_length=50)


class Color(models.Model):
    color_title = models.CharField(max_length=50)
    color_sort = models.IntegerField()
    color_image = models.CharField(max_length=100)
    color_group = models.ForeignKey(ColorGroup, models.DO_NOTHING)


class ProductColor(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING)
    color = models.ForeignKey(Color, models.DO_NOTHING)


class Volume(models.Model):
    volume_title = models.CharField(max_length=10)
    volume_sort = models.IntegerField()


class ProductVolumePrice(models.Model):
    volumeprice_price = models.CharField(max_length=10)
    volumeprice_volume = models.ForeignKey(Volume, models.DO_NOTHING)
    volumeprice_product = models.ForeignKey(Product, models.DO_NOTHING)
