# Generated by Django 3.1 on 2020-10-17 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0017_auto_20201017_0249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['product_vendor_code'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_description_title',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(upload_to='products/<django.db.models.query_utils.DeferredAttribute object at 0x7fef3c097df0>/', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price_option_extra_1',
            field=models.CharField(blank=True, default='Расход на м<sup>2</sup><br>(1 слой / 2 слоя)', max_length=50, null=True, verbose_name='Расширенная цена 3 столбик'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price_option_extra_2',
            field=models.CharField(blank=True, default='Цена за р/м<sup>2</sup><br>(1 слой / 2 слоя)', max_length=50, null=True, verbose_name='Расширенная цена 4 столбик'),
        ),
        migrations.CreateModel(
            name='ProductTab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tab_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название доп. вкладки')),
                ('tab_content', models.TextField(blank=True, null=True, verbose_name='Содержимое доп. вкладки')),
                ('tab_product', models.ManyToManyField(blank=True, to='Product.Product', verbose_name='Показывать в следующих товарах')),
            ],
        ),
    ]