from django.db import models


class Group(models.Model):
    """Объединяем слайды для главной страницы в группы, для удобства редактирования и хранения"""
    name = models.CharField(verbose_name='Название группы', max_length=50)

    class Meta:
        verbose_name = 'Группа слайдов'
        verbose_name_plural = 'Группы слайдов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Slide(models.Model):
    """Слайды на главной странице сайта"""

    slide_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    slide_img = models.ImageField(verbose_name='Изображение слайда', upload_to='index/slide/')
    slide_description = models.TextField(verbose_name='Текст / Описание (h2 / p)', blank=True, null=True)
    slide_link_name = models.CharField(verbose_name='Название кнопки', blank=True, null=True, max_length=100,
                                       default='Перейти')
    slide_link_url = models.CharField(verbose_name='Ссылка', blank=True, null=True, max_length=250)
    slide_order = models.IntegerField(verbose_name='Порядок', default='0')
    slide_visible = models.BooleanField(verbose_name='Показывать?', default=True)

    class Meta:
        ordering = ['slide_group', 'slide_order', 'id']
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return f'Слайд {self.id}'
