from django.shortcuts import render
from .models import Slide

def index(request):
    main_slides = Slide.objects.filter(slide_group=1, slide_visible=True)
    slides_2 = Slide.objects.filter(slide_group=2, slide_visible=True)
    banner = Slide.objects.filter(slide_group=3, slide_visible=True)[0]
    context = {
        'main_slides': main_slides,
        'slides_2': slides_2,
        'banner': banner
               }
    return render(request, 'index/index.html', context)