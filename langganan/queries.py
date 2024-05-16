from django.db import connection

def daftar_paket():
     with connection.cursor() as cursor:
        cursor.execute("SET search_path TO pacilflix")
        query = """
                SELECT p.nama, p.resolusi_layar, p.harga, dp.dukungan_perangkat
                FROM paket p
                JOIN dukungan_perangkat dp ON p.nama = dp.nama_paket
            """
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]
     
def daftar_langganan(username):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO pacilflix")
        cursor.execute("""
            SELECT p.nama, p.harga, p.resolusi_layar, dp.dukungan_perangkat, t.start_date_time, t.end_date_time
            FROM transaction t
            JOIN paket p ON t.nama_paket = p.nama
            JOIN pengguna pe ON t.username = pe.username
            JOIN dukungan_perangkat dp ON p.nama = dp.nama_paket
            WHERE t.start_date_time < NOW() AND NOW() < t.end_date_time AND t.username = %s;
        """, [username])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]
    
def daftar_transaksi(username):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO pacilflix")
        cursor.execute("""
            SELECT t.nama_paket, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran, p.harga
            FROM transaction t
            JOIN paket p ON t.nama_paket = p.nama
            JOIN pengguna pe ON t.username = pe.username
            JOIN dukungan_perangkat dp ON p.nama = dp.nama_paket
            WHERE t.username = %s;
        """, [username])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]
