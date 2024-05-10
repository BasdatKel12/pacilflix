import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages  
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from authentication.models import Profile

# Create your views here.

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:homepage")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def register (request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        negara = request.POST.get("negara")

        if password1 == password2:
            user = User.objects.filter(username=username)
            if len(user) == 0:
                user = User.objects.create_user(
                    username=username, password=password1)
                new_user = Profile(user = user, negara=negara)
                new_user.save()
                messages.success(request, 'Your account has been successfully created!')
                return redirect('authentication:login')
            else:
                messages.info(
                    request, 'Maaf, akun yang dibuat sudah pernah didaftarkan! Silahkan coba yang lain!')
                return redirect('authentication:register')
        else:
            messages.info(
                request, 'Sorry, incorrect username or password. Please try again.')
            return redirect('authentication:register')
    
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:landing-page'))
    response.delete_cookie('last_login')
    return response

def show_trailer(request):
    status = False
    if request.user.is_authenticated :
        status = True

    context = {
        'status': status
    }
    return render (request,"trailer.html",context)