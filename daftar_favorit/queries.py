from django.db import connection
from authentication.views import *

def favorite_list(request):
    
    username = request.COOKIES.get('username')
    
    with connection.cursor() as cursor:

        cursor.execute(rf"""
        SET search_path TO pacilflix;

        WITH ranked_favorites AS (
            SELECT 
                f.judul, 
                f.timestamp, 
                f.username,
                ROW_NUMBER() OVER (PARTITION BY f.username, f.judul ORDER BY f.timestamp) AS rn
            FROM daftar_favorit f
            WHERE f.judul IN ('Galau', 'Happy', 'Badmood') AND f.username = '{username}'
        )

        SELECT 
            rf.judul, 
            rf.timestamp, 
            rf.username
        FROM ranked_favorites rf
        WHERE rf.rn = 1;
        """)

        
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]

def favorite_details(request, username, list_judul):
    with connection.cursor() as cursor:
        cursor.execute(rf"""
        SET search_path TO pacilflix;
        WITH latest_entries AS (
            SELECT d.username, f.judul, d.id_tayangan, MAX(d.timestamp) AS latest_timestamp
            FROM tayangan_memiliki_daftar_favorit d
            JOIN daftar_favorit f ON d.username = f.username AND d.timestamp = f.timestamp
            WHERE d.username = '{username}'
            GROUP BY d.username, f.judul, d.id_tayangan
        )
        SELECT t.judul, d.timestamp, f.username, d.id_tayangan, f.judul AS judul_fav
        FROM daftar_favorit f
        JOIN tayangan_memiliki_daftar_favorit d 
          ON f.username = d.username 
         AND f.judul = '{list_judul}' 
         AND f.timestamp = d.timestamp
        JOIN tayangan t 
          ON d.id_tayangan = t.id
        JOIN latest_entries l 
          ON d.username = l.username 
         AND f.judul = l.judul
         AND d.id_tayangan = l.id_tayangan
         AND d.timestamp = l.latest_timestamp
        WHERE f.username = '{username}' 
          AND f.judul = '{list_judul}'
        """)

        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]


   
  
 
