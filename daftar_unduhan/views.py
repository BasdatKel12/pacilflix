from django.shortcuts import render

# Create your views here.
def unduhan(request):
    return render(request, 'daftar_unduhan.html')

