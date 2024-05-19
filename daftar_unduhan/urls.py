from django.urls import path, include
from daftar_unduhan.views import *

app_name = 'daftar_unduhan'

urlpatterns = [
    path('show_daftar_unduhan', show_daftar_unduhan, name = 'show_daftar_unduhan'),
    path('tambah_daftar_unduhan', tambah_daftar_unduhan),
    path('delete_unduhan', delete_unduhan, name = 'delete_unduhan'),
    path('add_unduhan/<str:id>', add_unduhan, name = 'add_unduhan')
]
