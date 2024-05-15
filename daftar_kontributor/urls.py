from django.urls import path

from daftar_kontributor.views import *

app_name = 'daftar_kontributor'

urlpatterns = [
    path('', show_daftar_kontributor, name = 'show_daftar_kontributor'),
]
