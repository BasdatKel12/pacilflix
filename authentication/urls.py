from django.urls import path, include
from authentication.views import login_user,logout_user,register


app_name = 'authentication'

urlpatterns = [
    path('login/', login_user, name = 'login'),
    path('register/', register, name = 'register'),
    path('logout/', logout_user, name = 'logout'),
]
