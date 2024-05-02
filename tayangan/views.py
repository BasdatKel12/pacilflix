from django.http import HttpResponse
from django.shortcuts import render

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