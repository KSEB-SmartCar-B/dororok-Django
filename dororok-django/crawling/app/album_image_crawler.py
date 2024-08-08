import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

#
# class GetSpotifyImage:
#     def __init__(self):
#         self.header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
#         }
#
#     async def fetch(self, session, url):
#         async with session.get(url, headers=self.header) as response:
#             return await response.text()
#
#     async def parse_track_image(self, session, track_id):
#         url = f'https://open.spotify.com/track/{track_id}'
#         html = await self.fetch(session, url)
#         parse = BeautifulSoup(html, "html.parser")
#
#         img_tag = parse.find('img')
#         if img_tag and 'src' in img_tag.attrs:
#             img_url = img_tag['src']
#         else:
#             img_url = 'photo/logo.png'
#         return img_url
#
#     async def parse_track_images(self, session, track_ids):
#         tasks = [self.parse_track_image(session, track_id) for track_id in track_ids]
#         return await asyncio.gather(*tasks)
#
import asyncio
import aiohttp
from bs4 import BeautifulSoup

class GetSpotifyImage:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
        }
        self.semaphore = asyncio.Semaphore(5)  # Limit concurrent requests

    async def fetch(self, session, url):
        async with session.get(url, headers=self.header) as response:
            return await response.text()

    async def parse_track_image(self, session, track_id):
        async with self.semaphore:  # Limit concurrent requests
            url = f'https://open.spotify.com/track/{track_id}'
            html = await self.fetch(session, url)
            parse = BeautifulSoup(html, "html.parser")

            img_tag = parse.find('img')
            if img_tag and 'src' in img_tag.attrs:
                img_url = img_tag['src']
            else:
                img_url = 'photo/logo.png'
            return img_url

    async def parse_track_images(self, session, track_ids):
        tasks = []
        for track_id in track_ids:
            tasks.append(self.parse_track_image(session, track_id))
        return await asyncio.gather(*tasks)
