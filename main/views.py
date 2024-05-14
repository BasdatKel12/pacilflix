from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def homepage(request):
    # print(request.COOKIES)
    if 'username' not in request.COOKIES:
        return HttpResponseRedirect(reverse("main:landing-page")) 
    
    context = {
        
    }

    return render(request, "homepage.html", context)

def landing_page(request):
    context = {

    }
    return render (request,"landing_page.html",context)