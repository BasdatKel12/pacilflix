from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='landing-page/')
def homepage(request):
    context = {

    }

    return render(request, "homepage.html", context)

def landing_page(request):
    context = {

    }
    return render (request,"landing_page.html",context)