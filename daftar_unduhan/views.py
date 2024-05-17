from django.shortcuts import render
from .queries import *
from django.db import connection

# Create your views here.
def show_daftar_unduhan(request):
    show_download_list = download_list(request)
    return render(request, 'daftar_unduhan.html', {'show_download_list': show_download_list})

def tambah_daftar_unduhan(request):
    return render(request, 'tambah_daftar_unduhan_modal.html')

def delete_unduhan(request):
    username = request.POST.get('username')
    id_tayangan = request.POST.get('id_tayangan')

    print(username)
    print(id_tayangan)

    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        DELETE FROM tayangan_terunduh u WHERE u.username = '{username}' AND u.id_tayangan = '{id_tayangan}'
        """)
    
    return HttpResponseRedirect(reverse('daftar_unduhan:show_daftar_unduhan'))

def add_unduhan(request):
    username = request.POST.get('username')
    
    id_tayangan = request.POST.get('id_tayangan')

    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        INSERT INTO tayangan_terunduh (timestamp, username, judul)
        VALUES ('{id_tayangan}', '{username}', NOW() );
        """)
    
    return HttpResponseRedirect(reverse('daftar_unduhan:show_daftar_unduhan'))