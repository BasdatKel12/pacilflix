from django.urls import path

from . import views

app_name = 'tayangan'

urlpatterns = [
    path("list/", views.list, name='list'),
    path("list/<int:isGlobal>", views.list_filter, name='list_filtered'),
    path("search/<str:judul>", views.search, name='search'),
    path("film/<str:id>", views.film, name='film'),
    path("series/<str:id>", views.series, name='series'),
    path("episode/<str:id>", views.episode, name='episode'),
    path('trailer/<int:isGlobal>', views.trailer_filter, name='trailer_filter'),
    path('trailer/', views.trailer, name = 'trailer'),
    path("add_ulasan/", views.add_ulasan, name='ulasan'),
    path("update_riwayat_nonton/", views.update_watchtime, name='update_riwayat'),
]