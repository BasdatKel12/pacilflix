from django.db import connection
from authentication.views import *

def favorite_list(request):
    
    username = request.COOKIES.get('username')
    
    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        SELECT f.judul, f.timestamp, f.username
            FROM daftar_favorit f
            WHERE f.username = '{username}';
        """)

        
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]

def favorite_details(request, username, list_judul, time):
    

    # username = request.POST.get('username')
    # # username = 'MaxAdventure22'
    # # list_judul = 'Galau'
    # list_judul = request.POST.get('judul')
    # time = request.POST.get('timestamp')

    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        SELECT t.judul, f.timestamp, f.username
            FROM daftar_favorit f
            JOIN tayangan_memiliki_daftar_favorit d ON f.username = '{username}' AND f.judul = '{list_judul}'
            JOIN tayangan t ON d.id_tayangan = t.id AND d.username = '{username}'
            WHERE f.username = '{username}' AND f.judul = '{list_judul}';

        """)

        
        result = cursor.fetchall()

        print(time)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]
        
   
  
 
