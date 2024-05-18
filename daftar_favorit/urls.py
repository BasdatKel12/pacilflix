from django.urls import path, include
from daftar_favorit.views import *

app_name = 'daftar_favorit'

urlpatterns = [
    path('show_daftar_favorit', show_daftar_favorit, name = 'show_daftar_favorit'),
    path('tambah_daftar_favorit', tambah_daftar_favorit),
    path('delete_favorit', delete_favorit, name = 'delete_favorit'),
    path('show_favorite_details', show_favorite_details, name = 'show_favorite_details'),
    path('add_favorit/<str:id>', add_favorit, name = 'add_favorit')
]
