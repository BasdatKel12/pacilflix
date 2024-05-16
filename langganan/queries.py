import datetime
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
            WHERE t.start_date_time < NOW() AND NOW() < t.end_date_time AND t.username = %s
            ORDER BY t.start_date_time DESC
            LIMIT 1;
        """, [username])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        print(columns)
        return [dict(zip(columns, row)) for row in result]
    
def daftar_transaksi(username):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO pacilflix")
        cursor.execute("""
            SELECT t.nama_paket, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran, p.harga
            FROM transaction t
            JOIN paket p ON t.nama_paket = p.nama
            JOIN pengguna pe ON t.username = pe.username
            WHERE t.username = %s;
        """, [username])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]

    
def get_paket(nama, dukungan_perangkat):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO pacilflix")
        cursor.execute("""
            SELECT p.nama, p.harga, p.resolusi_layar, dp.dukungan_perangkat
            FROM paket p
            JOIN dukungan_perangkat dp ON p.nama = dp.nama_paket
            WHERE p.nama = %s AND dp.dukungan_perangkat = %s;
        """, [nama, dukungan_perangkat])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]

def bayar_paket_post(username, nama, metode_pembayaran):
    date_now = datetime.datetime.now()
    end_date = date_now + datetime.timedelta(days=30)

    date_now_timestamp_str = date_now.strftime('%Y-%m-%d %H:%M:%S')
    date_now_str = date_now.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Asusmsi pada pembelian paket dengan durasi waktu 30 hari
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO pacilflix")
        cursor.execute("""
            INSERT INTO transaction (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [username,date_now_str, end_date_str, nama, metode_pembayaran, date_now_timestamp_str])

    print("Berhasil membeli paket!")
