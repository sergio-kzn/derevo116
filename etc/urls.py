from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_img_to_new_tab, name='cart'),
]