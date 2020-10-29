# Generated by Django 3.1 on 2020-10-18 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0024_auto_20201018_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='img_alt',
        ),
        migrations.AddField(
            model_name='product',
            name='product_img_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Подпись'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.CharField(blank=True, help_text='Введите цену без копеек и без знака рубля', max_length=30, null=True, verbose_name='Простая цена (Руб.)'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='img_title',
            field=models.CharField(max_length=100, verbose_name='Подпись'),
        ),
        migrations.AlterField(
            model_name='productvolumeprice',
            name='volumeprice_price',
            field=models.CharField(max_length=10, verbose_name='Цена'),
        ),
    ]