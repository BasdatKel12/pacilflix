from django.urls import path, include
from main.views import landing_page, homepage


app_name = 'main'

urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('landing-page/', landing_page, name = "landing-page")
]
