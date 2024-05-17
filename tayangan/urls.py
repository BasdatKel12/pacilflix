from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list),
    path("list/<int:isGlobal>", views.list_filter),
    path("search/<str:judul>", views.search),
    path("film/<str:id>", views.film),
    path("series/<str:id>", views.series),
    path("episode/<str:id>", views.episode),
    path('trailer/<int:isGlobal>', views.trailer_filter),
    path('trailer/', views.trailer, name = 'trailer'),
    path("add_ulasan/", views.add_ulasan),
    path("update_riwayat_nonton/", views.update_watchtime),
]