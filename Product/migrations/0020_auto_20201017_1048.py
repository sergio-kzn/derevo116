# Generated by Django 3.1 on 2020-10-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0019_auto_20201017_1037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producttab',
            options={'verbose_name': 'Вкладка', 'verbose_name_plural': 'Вкладки'},
        ),
        migrations.RemoveField(
            model_name='producttab',
            name='tab_product',
        ),
        migrations.AddField(
            model_name='product',
            name='product_tab',
            field=models.ManyToManyField(blank=True, to='Product.ProductTab', verbose_name='Доп. вкладки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(upload_to='products/<django.db.models.query_utils.DeferredAttribute object at 0x7fad682d2c70>/', verbose_name='Изображение товара'),
        ),
    ]