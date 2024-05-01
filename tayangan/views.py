from django.http import HttpResponse
from django.shortcuts import render

def list(request):
    return render(request, 'list.html')

def search(request):
    return render(request, 'search.html')