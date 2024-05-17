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

def favorite_details(request):

    username = request.POST.get('username')
    list_judul = request.POST.get('judul')

    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        SELECT f.judul, f.timestamp, f.username
            FROM daftar_favorit f
            JOIN tayangan_memiliki_daftar_favorit
            WHERE f.username = '{username}';
        """)

        
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]
        
   
  
 
