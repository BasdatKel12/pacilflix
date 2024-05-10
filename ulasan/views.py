from django.shortcuts import render

# Create your views here.
def ulasan(request):
    return render(request, 'ulasan.html')