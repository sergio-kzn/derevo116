# Generated by Django 3.1 on 2020-11-13 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0012_auto_20201113_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Cart.order', to_field='order_number', verbose_name='Заказ'),
        ),
    ]