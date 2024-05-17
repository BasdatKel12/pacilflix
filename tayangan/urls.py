from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list),
    path("search/<str:judul>", views.search),
    path("film/<str:id>", views.film),
    path("series/<str:id>", views.series),
    path("episode/<str:id>", views.episode),
    path('trailer/', views.show_trailer, name = 'trailer'),
    path("add_ulasan/", views.add_ulasan),
    path("update_riwayat_nonton/", views.update_watchtime),
]