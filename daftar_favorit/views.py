from django.shortcuts import render
from .queries import *
from django.db import connection

# Create your views here.
def show_favorite_details(request):
    show_details = favorite_details(request)

    return render(request, "daftar_favorit_details.html", {'show_details': show_details })

def show_daftar_favorit(request):
    show_favorite_list = favorite_list(request)
    
    return render(request, "daftar_favorit.html", {'show_favorite_list': show_favorite_list})

def tambah_daftar_favorit(request):
    return render(request, 'tambah_daftar_favorit_modal.html')

def delete_favorit(request):
    username = request.POST.get('username')
    judul = request.POST.get('judul')

    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        DELETE FROM daftar_favorit f WHERE f.username = '{username}' AND f.judul = '{judul}'
        """)
    
    return HttpResponseRedirect(reverse('daftar_favorit:show_daftar_favorit'))   

def add_favorit(request):
    username = request.POST.get('username')
    list_judul = request.POST.get('selectedText')
    id_tayangan = request.POST.get('id_tayangan')

    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        INSERT INTO daftar_favorit (timestamp, username, judul)
        VALUES (NOW(), '{username}', '{judul}' );

        INSERT INTO tayangan_memiliki_daftar_favorit (id_tayangan, timestamp, username)
        VALUES ('{id_tayangan}', NOW(), '{username}');
        """)
    
    return HttpResponseRedirect(reverse('daftar_favorit:show_daftar_favorit'))