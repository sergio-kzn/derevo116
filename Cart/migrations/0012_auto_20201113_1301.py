# Generated by Django 3.1 on 2020-11-13 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0011_order_order_delivery_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Cart.order', to_field='order_number', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_notification',
            field=models.BooleanField(default=0, verbose_name='Уведомлять по email?'),
        ),
    ]
