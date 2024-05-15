from django.db import connection

def filter_kontirbutor(choice):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO pacilflix")
        
        if choice == '1':
            query = """
                SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, 'Sutradara' AS role
                FROM contributors c
                JOIN sutradara s ON c.id = s.id
            """
            cursor.execute(query)
        elif choice == '2':
            query = """
                SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, 'Pemain' AS role
                FROM contributors c
                JOIN pemain p ON c.id = p.id
            """
            cursor.execute(query)
        elif choice == '3':
            query = """
                SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, 'Penulis skenario' AS role
                FROM contributors c
                JOIN penulis_skenario ps ON c.id = ps.id
            """
            cursor.execute(query)
        else:
            query = """
                SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan,
                CASE
                    WHEN s.id IS NOT NULL THEN 'Sutradara'
                    WHEN p.id IS NOT NULL THEN 'Pemain'
                    WHEN ps.id IS NOT NULL THEN 'Penulis skenario'
                END AS role
                FROM contributors c
                LEFT JOIN sutradara s ON c.id = s.id
                LEFT JOIN pemain p ON c.id = p.id
                LEFT JOIN penulis_skenario ps ON c.id = ps.id
            """
            cursor.execute(query)
        
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]
