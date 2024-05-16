from django.db import models

def parse_tuple_to_dict(data, cols: set):
    """
        Return list of dict if data is list
        Return None if no data
        Otherwise return dict
    """
    def parse_single_object(single_object):
        result = {}
        for inx, col in enumerate(cols):
            result[col] = single_object[inx]
        return result

    if type(data) is list:
        if len(data) == 0:
            return None
        return [parse_single_object(x) for x in data]
    if data is None: return None
    return parse_single_object(data)

# class Tayangan:
#     id: str
#     judul: str
#     sinopsis: str
#     asal_negara: str
#     sinopsis_trailer: str
#     url_video_trailer: str
#     release_date_trailer: str
#     id_sutradara: str


#     def from_tuple(tuple):
#         """
#             Return list of Tayangan or Tayangan matching tuple
#         """
#         def parse_single_object(tupleElm):
#             new_tayangan = Tayangan()
#             new_tayangan.id = tupleElm[0]
#             new_tayangan.judul = tupleElm[1]
#             new_tayangan.sinopsis = tupleElm[2]
#             new_tayangan.asal_negara = tupleElm[3]
#             new_tayangan.sinopsis_trailer = tupleElm[4]
#             new_tayangan.url_video_trailer = tupleElm[5]
#             new_tayangan.release_date_trailer = tupleElm[6]
#             new_tayangan.id_sutradara = tupleElm[7]
#             return new_tayangan
        
#         if type(tuple) is list:
#             return [parse_single_object(x) for x in tuple]
#         else:
#             return parse_single_object(tuple)
        
# class Film:
#     id_tayangan: str
#     deo_film: str
#     release_date_film: str
#     durasi_film: int

#     def from_tuple(tuple):
#         """
#             Return list of Tayangan or Tayangan matching tuple
#         """
#         def parse_single_object(tupleElm):
#             new_film = Film()
#             new_film.id_tayangan = tupleElm[0]
#             new_film.deo_film = tupleElm[1]
#             new_film.release_date_film = tupleElm[2]
#             new_film.durasi_film = tupleElm[3]
#             return new_film
        
#         if type(tuple) is list:
#             return [parse_single_object(x) for x in tuple]
#         else:
#             return parse_single_object(tuple)

# class Episode:
#     id_series: str
#     sub_judul: str
#     sinopsis: str
#     durasi: int
#     url_video: str
#     release_date: str

#     def from_tuple(tuple):
#         """
#             Return list of Tayangan or Tayangan matching tuple
#         """
#         def parse_single_object(tupleElm):
#             new_episode = Episode()
#             new_episode.id_series = tupleElm[0]
#             new_episode.sub_judul = tupleElm[1]
#             new_episode.sinopsis = tupleElm[2]
#             new_episode.durasi = tupleElm[3]
#             new_episode.url_video = tupleElm[4]
#             new_episode.release_date = tupleElm[5]
#             return new_episode
        
#         if type(tuple) is list:
#             return [parse_single_object(x) for x in tuple]
#         else:
#             return parse_single_object(tuple)