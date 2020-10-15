from django.shortcuts import render


def product(request, vendor, category, product):
    return render(request, 'product/product.html')


def category(request, vendor, category):
    return render(request,'product/category.html')

def all_category(request):
    return render(request,'product/category.html')
