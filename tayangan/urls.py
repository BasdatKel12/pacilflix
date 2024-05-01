from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list, name="index"),
    path("search/", views.search, name="index"),
]