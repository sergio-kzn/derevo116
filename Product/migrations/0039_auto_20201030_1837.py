# Generated by Django 3.1 on 2020-10-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0038_auto_20201030_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['img_sort']},
        ),
        migrations.AddField(
            model_name='productimage',
            name='img_sort',
            field=models.IntegerField(default=0, verbose_name='Сортировка'),
        ),
        migrations.AlterField(
            model_name='color',
            name='color_title',
            field=models.CharField(max_length=50, verbose_name='Подпись'),
        ),
        migrations.AlterField(
            model_name='colorgroup',
            name='color_group_name',
            field=models.CharField(help_text='Показывается только в админке.', max_length=100, verbose_name='Группа цветов'),
        ),
        migrations.AlterField(
            model_name='colorgroup',
            name='color_group_title',
            field=models.CharField(blank=True, help_text='Показывается во всплывающем окне при выборе цвета.<br>Если не заполнено, показывается название группы.', max_length=200, null=True, verbose_name='Заголовок'),
        ),
    ]
