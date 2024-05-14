from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def list(request):
    return render(request, 'list.html')

def search(request):
    return render(request, 'search.html')

def film(request):
    return render(request, 'view_film.html')

def series(request):
    return render(request, 'view_series.html')

def episode(request):
    return render(request, 'view_episode.html')

@csrf_exempt
def show_trailer(request):
    status = False
    if 'username' in request.COOKIES :
        status = True

    context = {
        'status': status
    }
    return render (request,"trailer.html",context)