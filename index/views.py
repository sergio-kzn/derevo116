from django.shortcuts import render

def index(request):
    context = {
        'context': "Hello",
               }
    return render(request, 'index/index.html', context)