from django.shortcuts import render
from .queries import *
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.
def show_daftar_unduhan(request):
    show_download_list = download_list(request)
    return render(request, 'daftar_unduhan.html', {'show_download_list': show_download_list})

def tambah_daftar_unduhan(request):
    return render(request, 'tambah_daftar_unduhan_modal.html')

@csrf_exempt
def delete_unduhan(request):
    username = request.POST.get('username')
    id_tayangan = request.POST.get('id_tayangan')
    try:
        with connection.cursor() as cursor:
            cursor.execute(rf"""SET search_path TO pacilflix;
            DELETE FROM tayangan_terunduh u WHERE u.username = '{username}' AND u.id_tayangan = '{id_tayangan}'
            """)
    except Exception as e:
        messages.error(request, "Unduhan tidak dapat dihapus.")
        return HttpResponseRedirect(reverse('daftar_unduhan:show_daftar_unduhan'))
    
    return HttpResponseRedirect(reverse('daftar_unduhan:show_daftar_unduhan'))

@csrf_exempt
def add_unduhan(request, id: str):
    username = request.COOKIES.get('username')
    # id_tayangan = request.POST.get('id_tayangan')

    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        INSERT INTO tayangan_terunduh(id_tayangan, username, timestamp)
        VALUES ('{id}', '{username}', NOW() );
        """)
    
    return HttpResponseRedirect(reverse('daftar_unduhan:show_daftar_unduhan'))