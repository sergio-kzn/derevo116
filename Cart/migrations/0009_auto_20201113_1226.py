# Generated by Django 3.1 on 2020-11-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0008_auto_20201113_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_order',
            field=models.CharField(max_length=255, verbose_name='Заказ'),
        ),
    ]
