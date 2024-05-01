from django.urls import path, include
from authentication.views import login_user, register, show_trailer, logout_user


app_name = 'authentication'

urlpatterns = [
    path('login/', login_user, name = 'login'),
    path('register/', register, name = 'register'),
    path('logout/', logout_user, name = 'logout'),
    path('trailer/', show_trailer, name = 'trailer')
]
