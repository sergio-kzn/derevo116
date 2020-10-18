# Generated by Django 3.1 on 2020-10-16 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0011_auto_20201016_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_description_title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Название вкладки'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_extra_desc',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительная информация рядом с ценой'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительная вкладка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(upload_to='products/<django.db.models.query_utils.DeferredAttribute object at 0x7fe09da23bb0>/', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='category_url',
            field=models.SlugField(unique=True, verbose_name='Ссылка url (проверьте vendor_url)'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='volume_sort',
            field=models.IntegerField(default=0, verbose_name='Сортировка'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='volume_title',
            field=models.CharField(max_length=10, verbose_name='Опция'),
        ),
    ]
