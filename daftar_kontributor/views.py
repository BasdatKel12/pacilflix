from django.shortcuts import render
from .queries import *


def show_daftar_kontributor(request):
    choice = request.GET.get('filter_choice', None)
    daftar_kontributor = filter_kontirbutor(choice)
    return render(request, "daftar_kontributor.html", {'daftar_kontributor': daftar_kontributor})
