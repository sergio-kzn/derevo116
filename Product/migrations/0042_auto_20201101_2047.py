# Generated by Django 3.1 on 2020-11-01 17:47

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0041_optiongroup_options_sort'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='color_html',
            field=models.CharField(blank=True, help_text='Цвет в формате HEX, например: "#ebe7e0"', max_length=20, null=True, verbose_name='Цвет HEX'),
        ),
        migrations.AlterField(
            model_name='color',
            name='color_image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='products/colors', verbose_name='Изображение'),
        ),
    ]
