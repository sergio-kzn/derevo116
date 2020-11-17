from django.shortcuts import render
import re

def convert_img_to_new_tab(request):
    content = {}

    if request.method == 'POST':
        source = request.POST['source']
        result = request.POST['source']
        result = result.replace('<p>', "")
        result = result.replace('</p>', "")
        result = result.replace('<br>', "")
        result = result.replace('<img src=', "\n\n<img src=")
        result = re.sub(r" style=\".*\"", "", result)
        result = re.split(r'\n\n', result)
        result.remove("")

        for index in range(0, len(result)):
            result[index] = result[index]*2
            result[index] = result[index].replace("<img src=", '<a data-caption="" data-fancybox="gallery" href=', 1)
            result[index] = result[index].replace("<img src=", '\n<img alt="" class="img-fluid" src=', 1)
            result[index] = '<div class="col px-0">\n' + result[index] + "\n</a>\n</div>"
        result.insert(0, '<div class="row row-cols-2 row-cols-lg-3">')
        result.append('</div>')


        result = ''.join(str(e + '\n\n') for e in result)
        print(result)
        content = {'convert_img_to_new_tab': result,
                   'source': source}

    return render(request, 'etc/convert_img_to_new_tab.html', content)
