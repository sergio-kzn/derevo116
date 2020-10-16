from django.db import models

class SimplePage(models.Model):
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return str(self.simple_page_title)
    simple_page_title = models.CharField(verbose_name='Заголовок', max_length=100)
    simple_page_context = models.TextField(verbose_name='Описание')
    simple_page_url = models.SlugField(verbose_name='Ссылка url', unique=True)