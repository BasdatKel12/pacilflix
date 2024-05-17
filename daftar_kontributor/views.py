from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .queries import *


def show_daftar_kontributor(request):
    try:
        username = request.COOKIES['username']
    except:
        return HttpResponseRedirect(reverse("authentication:login"))
    choice = request.GET.get('filter_choice', None)
    daftar_kontributor = filter_kontirbutor(choice)
    return render(request, "daftar_kontributor.html", {'daftar_kontributor': daftar_kontributor})
