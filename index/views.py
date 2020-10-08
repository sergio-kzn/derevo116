from django.shortcuts import render
from .models import Slide

def index(request):
    main_slides = Slide.objects.filter(slide_group=1, slide_visible=True)

    context = {
        'main_slides': main_slides,
               }
    return render(request, 'index/index.html', context)