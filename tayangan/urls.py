from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list),
    path("search/", views.search),
    path("film/", views.film),
    path("series/", views.series),
    path("episode/", views.episode)
]