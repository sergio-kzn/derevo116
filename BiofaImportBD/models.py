# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSummernoteAttachment(models.Model):
    file = models.CharField(max_length=100)
    uploaded = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_summernote_attachment'


class MainpageGroupslider(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'mainpage_groupslider'


class MainpageSimplepage(models.Model):
    simple_page_title = models.CharField(max_length=100)
    simple_page_context = models.TextField()
    simple_page_url = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'mainpage_simplepage'


class MainpageSlider(models.Model):
    slider_img = models.CharField(max_length=100)
    slider_title = models.CharField(max_length=10, blank=True, null=True)
    slider_description = models.TextField(blank=True, null=True)
    slider_button = models.CharField(max_length=10)
    slider_group = models.ForeignKey(MainpageGroupslider, models.DO_NOTHING, blank=True, null=True)
    slider_button_href = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mainpage_slider'


class NewsNews(models.Model):
    news_title = models.CharField(max_length=100)
    news_date = models.DateField()
    news_mainpage = models.BooleanField()
    news_description = models.CharField(max_length=200)
    news_content = models.TextField()
    news_img = models.CharField(max_length=100)
    news_url = models.CharField(unique=True, max_length=50)
    news_tags = models.ForeignKey('NewsNewstag', models.DO_NOTHING, blank=True, null=True)
    news_img_preview = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'news_news'


class NewsNewstag(models.Model):
    news_tag_title = models.CharField(max_length=10)
    news_tag_url = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'news_newstag'


class PortfolioPortfolio(models.Model):
    portfolio_img = models.CharField(max_length=100)
    portfolio_sort = models.IntegerField()
    portfolio_category = models.ForeignKey('PortfolioPortfoliocategory', models.DO_NOTHING)
    portfolio_img_preview = models.CharField(max_length=100)
    portfolio_title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portfolio_portfolio'


class PortfolioPortfoliocategory(models.Model):
    portfolio_category_img = models.CharField(max_length=100)
    portfolio_category_url = models.CharField(unique=True, max_length=50)
    portfolio_category_sort = models.IntegerField()
    portfolio_category_title = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'portfolio_portfoliocategory'


class ProductAttributeproduct(models.Model):
    attribute_title = models.CharField(max_length=200)
    attribute_sort = models.IntegerField()
    attribute_product = models.ForeignKey('ProductProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product_attributeproduct'


class ProductCategoryproduct(models.Model):
    category_sort = models.IntegerField()
    category_url = models.CharField(unique=True, max_length=50)
    category_title = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'product_categoryproduct'


class ProductColorproduct(models.Model):
    color_title = models.CharField(max_length=50)
    color_sort = models.IntegerField()
    color_image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'product_colorproduct'


class ProductProduct(models.Model):
    product_title = models.CharField(max_length=60)
    product_img = models.CharField(max_length=100)
    product_description = models.TextField(blank=True, null=True)
    product_content = models.TextField()
    product_url = models.CharField(unique=True, max_length=50)
    product_file = models.CharField(max_length=100, blank=True, null=True)
    product_category = models.ForeignKey(ProductCategoryproduct, models.DO_NOTHING, blank=True, null=True)
    product_price = models.CharField(max_length=30, blank=True, null=True)
    product_vendor_code = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'product_product'


class ProductProductProductColor(models.Model):
    product = models.ForeignKey(ProductProduct, models.DO_NOTHING)
    colorproduct = models.ForeignKey(ProductColorproduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product_product_product_color'
        unique_together = (('product', 'colorproduct'),)


class ProductVolumepriceproduct(models.Model):
    volumeprice_price = models.CharField(db_column='volumePrice_price', max_length=10)  # Field name made lowercase.
    volumeprice_volume = models.ForeignKey('ProductVolumeproduct', models.DO_NOTHING, db_column='volumePrice_volume_id')  # Field name made lowercase.
    volumeprice_product = models.ForeignKey(ProductProduct, models.DO_NOTHING, db_column='volumePrice_Product_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_volumepriceproduct'


class ProductVolumepriceproductgroup(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'product_volumepriceproductgroup'


class ProductVolumeproduct(models.Model):
    volume_title = models.CharField(max_length=10)
    volume_sort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_volumeproduct'


class SqliteStat1(models.Model):
    tbl = models.TextField(blank=True, null=True)  # This field type is a guess.
    idx = models.TextField(blank=True, null=True)  # This field type is a guess.
    stat = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sqlite_stat1'


class SqliteStat4(models.Model):
    tbl = models.TextField(blank=True, null=True)  # This field type is a guess.
    idx = models.TextField(blank=True, null=True)  # This field type is a guess.
    neq = models.TextField(blank=True, null=True)  # This field type is a guess.
    nlt = models.TextField(blank=True, null=True)  # This field type is a guess.
    ndlt = models.TextField(blank=True, null=True)  # This field type is a guess.
    sample = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sqlite_stat4'


class WhatgoingpaintWhatgoingpaint(models.Model):
    what_title = models.CharField(max_length=150)
    what_img = models.CharField(max_length=100)
    what_sort = models.IntegerField()
    what_url = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'whatgoingpaint_whatgoingpaint'


class WhatgoingpaintWhatgoingpaintsubcategory(models.Model):
    subcategory_img = models.CharField(max_length=100, blank=True, null=True)
    subcategory_title = models.CharField(max_length=50)
    subcategory_h1 = models.CharField(max_length=200, blank=True, null=True)
    subcategory_content = models.TextField(blank=True, null=True)
    subcategory_url = models.CharField(unique=True, max_length=50)
    subcategory_sort = models.IntegerField()
    subcategory_main_category = models.ForeignKey(WhatgoingpaintWhatgoingpaint, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'whatgoingpaint_whatgoingpaintsubcategory'
