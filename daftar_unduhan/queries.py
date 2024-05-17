from django.db import connection
from authentication.views import *

def download_list(request):
    username = request.COOKIES.get('username')
    
    with connection.cursor() as cursor:
        cursor.execute(rf"""SET search_path TO pacilflix;
        SELECT t.judul, u.timestamp, u.id_tayangan, u.username
            FROM tayangan_terunduh u
            JOIN tayangan t ON u.id_tayangan = t.id
            WHERE u.username = '{username}';
        """)
    

        
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]

       