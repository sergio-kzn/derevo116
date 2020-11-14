from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_order, name='search_order'),
    path('select_payment/', views.select_payment, name='select_payment'),
    path('success/', views.success, name='success'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('deletefromcart/', views.delete_from_cart, name='delete_from_cart'),
    path('addtocart/', views.add_to_cart, name='add_to_cart'),
    path('confirm/', views.confirm, name='confirm'),
    path('', views.cart, name='cart'),
]