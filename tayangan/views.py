from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
import datetime
import json

@csrf_exempt
def add_ulasan(request):
    # TODO: Filter Login
    
    # username = request.COOKIE['username']
    username = 'LilyDreamer87'
    if request.method == 'POST':
        data = json.loads(request.body)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        id_tayangan = data['id_tayangan']
        rating = data['rating']
        deskripsi = data['deskripsi']

        with connection.cursor() as cursor:
            # Get User Paket
            cursor.execute(rf"""
            SET search_path to pacilflix;
            INSERT INTO
            ulasan (username, timestamp, id_tayangan, rating, deskripsi)
            VALUES
            (
            '{username}',
            '{timestamp}',
            '{id_tayangan}',
            {rating},
            '{deskripsi}'
            );
            """)
        
        return HttpResponse({'status': 'OK'})

    return HttpResponse({'status': 'INVALID METHOD'})

def list(request):
    # if 'username' not in request.COOKIES :
        # return HttpResponseRedirect(reverse('authentication:login'))
    
    # username = request.POST.get("username")
    username = 'LilyDreamer87'
    # TODO : FIX HARDCODING
    with connection.cursor() as cursor:
        # Get User Paket
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT * FROM transaction 
        WHERE username='{username}' AND CURRENT_DATE <= end_date_time;
        """)
        columns = ("username","start_date_time","end_date_time","nama_paket","metode_pembayaran","timestamp_pembayaran")
        list_paket = parse_tuple_to_dict(cursor.fetchall(), columns)
        active_paket = 0 if not list_paket else len(list_paket) > 0

        # Semua Film
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        SELECT * FROM film as F
        LEFT JOIN tayangan as T ON T.id=F.id_tayangan;
        """)
        columns = ("id_tayangan", "url_video_film" ,"release_date_film" ,"durasi_film" ,"id" ,"judul" ,"sinopsis" ,"asal_negara" ,"sinopsis_trailer" ,"url_video_trailer" ,"release_date_trailer" ,"id_sutradara")
        list_film = parse_tuple_to_dict(cursor.fetchall(), columns)

        # Semua Series
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        SELECT * FROM series as S
        LEFT JOIN tayangan as T ON T.id=S.id_tayangan;
        """)
        columns = ("id_tayangan","id","judul","sinopsis","asal_negara","sinopsis_trailer","url_video_trailer","release_date_trailer","id_sutradara")
        list_series = parse_tuple_to_dict(cursor.fetchall(), columns)

    context = {
        'active_paket' : active_paket,
        'list_film' : list_film,
        'list_series' : list_series
    }
    return render(request, 'list.html', context=context)

def search(request, judul: str):
    # Search
    with connection.cursor() as cursor:
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT 
        T.*, 
        CASE
            WHEN EXISTS (SELECT * FROM film F WHERE F.id_tayangan=T.id)
            THEN True
            ELSE False
        END AS is_film
        FROM tayangan T
        WHERE judul ilike '%{judul}%';
        """)
        columns = ("id","judul","sinopsis","asal_negara","sinopsis_trailer","url_video_trailer","release_date_trailer","id_sutradara","is_film")
        results = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

    context = {
        'results' : results
    }

    return render(request, 'search.html', context)

def film(request, id: str):
    # TODO: FIX BUTTON TONTON, DOWNLOAD, AND FAVORITE IN FILM
    
    with connection.cursor() as cursor:
        # Get Film
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        WITH filtered_film AS (
        SELECT * FROM film
        WHERE film.id_tayangan='{id}'
        )

        SELECT * FROM filtered_film F
        LEFT JOIN tayangan T ON F.id_tayangan=T.id;
        """)
        columns = ("id_tayangan","url_video_film","release_date_film","durasi_film","id","judul","sinopsis","asal_negara","sinopsis_trailer","url_video_trailer","release_date_trailer","id_sutradara")
        film = parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]

        # Get Total View Film
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        SELECT COALESCE(
        (SELECT COUNT(*) FROM riwayat_nonton
        WHERE id_tayangan='{id}')
        ,
        0
        ) as count
        """)
        columns = ("count",)
        total_views = parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]['count']

        # Get Average Rating Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT COALESCE(
        (SELECT AVG(rating) FROM ulasan
        WHERE id_tayangan='{id}')
        ,
        0
        ) AS avg
        """)
        columns = ("avg",)
        rating_avg = float(parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]['avg'])

        # Get Genre Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT DISTINCT genre FROM genre_tayangan
        WHERE id_tayangan='{id}';
        """)
        columns = ("genre",)
        list_genre = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

        # Get Pemain Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        WITH pemain_tayangan AS
        (SELECT * FROM memainkan_tayangan M
        WHERE id_tayangan='{id}')

        SELECT * FROM pemain_tayangan
        LEFT JOIN contributors C ON C.id=id_pemain;
        """)
        columns = ("id_tayangan","id_pemain","id","nama","jenis_kelamin","kewarganegaraan")
        list_pemain = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

        # Get Skenario Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        WITH skenario_tayangan AS
        (SELECT * FROM menulis_skenario_tayangan M
        WHERE id_tayangan='{id}')

        SELECT * FROM skenario_tayangan
        LEFT JOIN contributors C ON C.id=id_penulis_skenario;
        """)
        columns = ("id_tayangan","id_penulis_skenario","id","nama","jenis_kelamin","kewarganegaraan")
        list_skenario = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

        # Get Sutradara Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        WITH tayangan_detail AS
        (SELECT * FROM tayangan T
        WHERE id='{id}')

        SELECT nama FROM tayangan_detail
        LEFT JOIN contributors C ON C.id=id_sutradara;
        """)
        columns = ("nama",) 
        sutradara = parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]

        # Get Ulasan
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT * FROM ulasan
        WHERE id_tayangan='{id}'
        ORDER BY timestamp;
        """)
        columns = ("id_tayangan","username","timestamp","rating","deskripsi")
        list_ulasan = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

    context = {
        'film' : film,
        'total_views' : total_views,
        'rating_avg' : rating_avg,
        'list_genre' : list_genre,
        'list_pemain' : list_pemain,
        'list_skenario' : list_skenario,
        'sutradara' : sutradara,
        'list_ulasan' : list_ulasan
    }    
    
    return render(request, 'view_film.html', context=context)

def series(request, id: str):
    with connection.cursor() as cursor:
        # Get Series
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        WITH filtered_series AS (
        SELECT * FROM series
        WHERE series.id_tayangan='{id}'
        )

        SELECT * FROM filtered_series F
        LEFT JOIN tayangan T ON F.id_tayangan=T.id;
        """)
        columns = ("id_tayangan","id","judul","sinopsis","asal_negara","sinopsis_trailer","url_video_trailer","release_date_trailer","id_sutradara")
        series = parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]

        # Get Episode Series
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        SELECT * FROM episode
        WHERE id_series='{id}'
        ORDER BY release_date
        """)
        columns = ("id_series","sub_judul","sinopsis","durasi","url_video","release_date")
        list_episode = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

        # Get Total View Film
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        SELECT COALESCE(
        (SELECT COUNT(*) FROM riwayat_nonton
        WHERE id_tayangan='{id}')
        ,
        0
        ) as count
        """)
        columns = ("count",)
        total_views = parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]['count']

        # Get Average Rating Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT COALESCE(
        (SELECT AVG(rating) FROM ulasan
        WHERE id_tayangan='{id}')
        ,
        0
        ) AS avg
        """)
        columns = ("avg",)
        rating_avg = float(parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]['avg'])

        # Get Genre Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT DISTINCT genre FROM genre_tayangan
        WHERE id_tayangan='{id}';
        """)
        columns = ("genre",)
        list_genre = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

        # Get Pemain Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        WITH pemain_tayangan AS
        (SELECT * FROM memainkan_tayangan M
        WHERE id_tayangan='{id}')

        SELECT * FROM pemain_tayangan
        LEFT JOIN contributors C ON C.id=id_pemain;
        """)
        columns = ("id_tayangan","id_pemain","id","nama","jenis_kelamin","kewarganegaraan")
        list_pemain = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

        # Get Skenario Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        WITH skenario_tayangan AS
        (SELECT * FROM menulis_skenario_tayangan M
        WHERE id_tayangan='{id}')

        SELECT * FROM skenario_tayangan
        LEFT JOIN contributors C ON C.id=id_penulis_skenario;
        """)
        columns = ("id_tayangan","id_penulis_skenario","id","nama","jenis_kelamin","kewarganegaraan")
        list_skenario = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

        # Get Sutradara Film
        cursor.execute(rf"""
        SET search_path to pacilflix;
        WITH tayangan_detail AS
        (SELECT * FROM tayangan T
        WHERE id='{id}')

        SELECT nama FROM tayangan_detail
        LEFT JOIN contributors C ON C.id=id_sutradara;
        """)
        columns = ("nama",) 
        sutradara = parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]

        # Get Ulasan
        cursor.execute(rf"""
        SET search_path to pacilflix;
        SELECT * FROM ulasan
        WHERE id_tayangan='{id}'
        ORDER BY timestamp;
        """)
        columns = ("id_tayangan","username","timestamp","rating","deskripsi")
        list_ulasan = parse_tuple_to_dict(cursor.fetchall(), cols=columns)

    context = {
        'series' : series,
        'list_episode' : list_episode,
        'total_views' : total_views,
        'rating_avg' : rating_avg,
        'list_genre' : list_genre,
        'list_pemain' : list_pemain,
        'list_skenario' : list_skenario,
        'sutradara' : sutradara,
        'list_ulasan' : list_ulasan
    }

    return render(request, 'view_series.html', context)

def episode(request, id: str):
    # TODO: ADD SLIDER & SIMPAN RIWAYAT TONTON
    id_series = id[:id.rfind('-')]
    id_episode = int(id[id.rfind('-')+1:])

    with connection.cursor() as cursor:
        # Get Series
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        WITH filtered_series AS (
        SELECT * FROM series
        WHERE series.id_tayangan='{id_series}'
        )

        SELECT * FROM filtered_series F
        LEFT JOIN tayangan T ON F.id_tayangan=T.id;
        """)
        columns = ("id_tayangan","id","judul","sinopsis","asal_negara","sinopsis_trailer","url_video_trailer","release_date_trailer","id_sutradara")
        series = parse_tuple_to_dict(cursor.fetchall(), cols=columns)[0]

        # Get Episode Series
        cursor.execute(rf"""
        SET search_path to pacilflix; 
        SELECT * FROM episode
        WHERE id_series='{id_series}'
        ORDER BY release_date
        """)
        columns = ("id_series","sub_judul","sinopsis","durasi","url_video","release_date")
        list_episode = parse_tuple_to_dict(cursor.fetchall(), cols=columns)
        this_episode = list_episode[id_episode-1]

    context = {
        'serie' : series,
        'list_episode' : list_episode,
        'episode' : this_episode
    }
    print(this_episode)

    return render(request, 'view_episode.html', context=context)

@csrf_exempt
def show_trailer(request):
    if request.method == 'GET':        
        with connection.cursor() as cursor:
            # TODO
            # Fetch Top 10

            # Semua Film
            cursor.execute(rf"""
            SET search_path to pacilflix; 
            SELECT * FROM film as F
            LEFT JOIN tayangan as T ON T.id=F.id_tayangan;
            """)
            columns = ("id_tayangan", "url_video_film" ,"release_date_film" ,"durasi_film" ,"id" ,"judul" ,"sinopsis" ,"asal_negara" ,"sinopsis_trailer" ,"url_video_trailer" ,"release_date_trailer" ,"id_sutradara")
            list_film = parse_tuple_to_dict(cursor.fetchall(), columns)

            # Semua Series
            cursor.execute(rf"""
            SET search_path to pacilflix; 
            SELECT * FROM series as S
            LEFT JOIN tayangan as T ON T.id=S.id_tayangan;
            """)
            columns = ("id_tayangan","id","judul","sinopsis","asal_negara","sinopsis_trailer","url_video_trailer","release_date_trailer","id_sutradara")
            list_series = parse_tuple_to_dict(cursor.fetchall(), columns)

    status = False # TODO understand maksud kemal status
    if 'username' in request.COOKIES :
        status = True

    context = {
        'status': status,
        'list_film': list_film,
        'list_series': list_series
    }
    return render (request, "trailer.html", context)