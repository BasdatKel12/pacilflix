from django.urls import path

from langganan.views import *

app_name = 'langganan'

urlpatterns = [
    path('', show_langganan_page, name = 'show_langganan_page'),
]
