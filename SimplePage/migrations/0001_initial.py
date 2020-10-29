# Generated by Django 3.1 on 2020-10-27 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimplePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simple_page_title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('simple_page_context', models.TextField(verbose_name='Описание')),
                ('simple_page_url', models.SlugField(unique=True, verbose_name='Ссылка url')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
            },
        ),
    ]