from django.urls import path, include
from . import views

app_name = 'daftar_unduhan'

urlpatterns = [
    path('unduhan', views.unduhan)
]
