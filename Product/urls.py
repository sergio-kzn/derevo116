"""Derevo116 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from Index import views as index
from . import views


urlpatterns = [
    # path('biofa/', include('BiofaImportBD.urls'), name='biofa_paints'),
    path('<slug:root_url>/<slug:vendor_url>/<slug:category_url>/<slug:product_url>/', views.product, name='product-url'),
    path('<slug:root_url>/<slug:vendor_url>/<slug:category_url>/', views.category, name='category-url'),
    path('<slug:root_url>/<slug:vendor_url>/', views.vendor_category, name='vendor-category-url'),
    path('<slug:root_url>/', views.root_category, name='root-category-url'),
    # path('', views.root_category, name='root-category'),
    # path('', index.index),

]
