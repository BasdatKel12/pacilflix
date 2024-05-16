from django.urls import path

from langganan.views import *

app_name = 'langganan'

urlpatterns = [
    path('', show_langganan_page, name = 'show_langganan_page'),
    path('beli/<str:nama_paket>/<str:dukungan_perangkat>/', show_beli_page, name='show_beli_page'),
    path('beli/<str:nama_paket>/<str:dukungan_perangkat>/bayar/', bayar_paket, name='bayar_paket'),
]
