from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .queries import *

def show_langganan_page(request):
    try:
        username = request.COOKIES['username']
    except:
        return HttpResponseRedirect(reverse("authentication:login"))
    daftar_paket_list = daftar_paket()
    daftar_langganan_list = daftar_langganan(username)
    daftar_transaksi_list = daftar_transaksi(username)
    return render(request, "kelola_langganan.html", {'daftar_paket': daftar_paket_list, 
                                                     'daftar_langganan' : daftar_langganan_list,
                                                     'daftar_transaksi' : daftar_transaksi_list})

def show_beli_page(request):
    try:
        username = request.COOKIES['username']
    except:
        return HttpResponseRedirect(reverse("authentication:login"))
    return render(request, "halaman_beli.html")