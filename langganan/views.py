from django.shortcuts import render

def show_langganan_page(request):
    return render(request, "kelola_langganan.html")
