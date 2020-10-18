# Generated by Django 3.1 on 2020-10-17 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0020_auto_20201017_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttab',
            name='tab_title_admin',
            field=models.CharField(default='', max_length=200, verbose_name='Название (в админке)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(upload_to='products', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='producttab',
            name='tab_title',
            field=models.CharField(max_length=200, verbose_name='Название (в шаблоне)'),
        ),
    ]
