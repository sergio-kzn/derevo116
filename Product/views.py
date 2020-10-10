from django.shortcuts import render


def product(request, category, product):

    return render(request, 'product/product.html')

def category(request, category):

    return render(request,'product/category.html')
