# Generated by Django 3.1 on 2020-11-13 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0010_status_status_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_delivery_other',
            field=models.TextField(blank=True, null=True, verbose_name='Своя доставка'),
        ),
    ]
