# import aiohttp
#
# from spotify.authentication.spotify_auth import get_spotify_client
# from crawling.app.album_image_crawler import GetSpotifyImage
#
#
# class SearchSpotifyMusic:
#     def __init__(self):
#         self.sp = get_spotify_client()
#
#     async def search_music(self, title, artist):
#         track_names = []
#         artist_names = []
#         track_ids = []
#
#         if not title:
#             track_results = self.sp.search(q=f"artist:{artist}", limit=10, type='track', market='KR')
#         elif not artist:
#             track_results = self.sp.search(q=f"track:{title}", limit=10, type='track', market='KR')
#         else:
#             track_results = self.sp.search(q=f"track:{title} artist:{artist}", limit=10, type='track', market='KR')
#
#         while track_results:
#             for item in track_results['tracks']['items']:
#                 track_id = item['id']
#                 track_name = item['name']
#                 artist_name = item['artists'][0]['name']
#                 track_ids.append(track_id)
#                 track_names.append(track_name)
#                 artist_names.append(artist_name)
#
#             if track_results['tracks']['next']:
#                 track_results = self.sp.next(track_results['tracks'])
#             else:
#                 track_results = None
#         async with aiohttp.ClientSession() as session:
#             track_images = await GetSpotifyImage().parse_track_images(session, track_ids)
#
#         return track_ids, track_names, artist_names, track_images
#
#
# async def get_music_data(input_title, input_artist):
#     title = input_title
#     artist = input_artist
#
#     searcher = SearchSpotifyMusic()
#     track_ids, track_names, artist_names, track_images = await searcher.search_music(title, artist)
#     return track_names, artist_names, track_ids, track_images

import asyncio
import aiohttp
from spotify.authentication.spotify_auth import get_spotify_client
from crawling.app.album_image_crawler import GetSpotifyImage


class SearchSpotifyMusic:
    def __init__(self):
        self.sp = get_spotify_client()

    async def search_music(self, title, artist):
        track_names = []
        artist_names = []
        track_ids = []

        if not title:
            track_results = self.sp.search(q=f"artist:{artist}", limit=10, type='track', market='KR')
        elif not artist:
            track_results = self.sp.search(q=f"track:{title}", limit=10, type='track', market='KR')
        else:
            track_results = self.sp.search(q=f"track:{title} artist:{artist}", limit=10, type='track', market='KR')

        while track_results:
            for item in track_results['tracks']['items']:
                track_id = item['id']
                track_name = item['name']
                artist_name = item['artists'][0]['name']
                track_ids.append(track_id)
                track_names.append(track_name)
                artist_names.append(artist_name)

            if track_results['tracks']['next']:
                track_results = self.sp.next(track_results['tracks'])
            else:
                track_results = None

        async with aiohttp.ClientSession() as session:
            get_spotify_image = GetSpotifyImage()
            track_images = await get_spotify_image.parse_track_images(session, track_ids)

        return track_ids, track_names, artist_names, track_images


async def get_music_data(input_title, input_artist):
    title = input_title
    artist = input_artist

    searcher = SearchSpotifyMusic()
    track_ids, track_names, artist_names, track_images = await searcher.search_music(title, artist)
    return track_names, artist_names, track_ids, track_images
