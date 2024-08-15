import re
import time

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from crawling.models import crawling_genre_model


TARGET_COUNT = 1000

genre_code_map = {
    '발라드': 'GN0100',
    '댄스': 'GN0200',
    '인디': 'GN0500',
    '트로트': 'GN0700',
    'OST': 'GN1500',
    'POP': 'GN0900',
    'JPOP': 'GN1900',
    '재즈': 'GN1700',
    '클래식': 'GN1600',
    '뉴에이지': 'GN1800',
    '일렉트로니카': 'GN1100',
    '국내 밴드': 'GN0600',
    '해외 밴드': 'GN1200',
    '국내 록메탈': 'GN0600',
    '해외 록메탈': 'GN1000',
    '국내 랩힙합': 'GN0300',
    '해외 랩힙합': 'GN1200',
    '국내 RBSOUL': 'GN0400',
    '해외 RBSOUL': 'GN1300',
    '국내 포크블루스': 'GN0800',
    '해외 포크블루스컨트리': 'GN1400',
}


class MelonGenreList:
    def __init__(self, genre_code, pages):
        self.genre_code = genre_code
        self.pages = pages
        self.driver = webdriver.Chrome()

    def get_music_data(self, start_index, url_index):
        urls = [
            f'https://www.melon.com/genre/song_list.htm?gnrCode={self.genre_code}&steadyYn=Y#params%5BgnrCode%5D={self.genre_code}&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=NEW&params%5BsteadyYn%5D=Y&po=pageObj&startIndex={start_index}',
            f'https://www.melon.com/genre/song_list.htm?gnrCode={self.genre_code}&dtlGnrCode=#params%5BgnrCode%5D={self.genre_code}&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=NEW&params%5BsteadyYn%5D=N&po=pageObj&startIndex={start_index}'
        ]

        try:
            self.driver.get(urls[url_index])
            time.sleep(2)

            html = self.driver.page_source
            parse = BeautifulSoup(html, 'html.parser')

            titles = parse.find_all("div", {"class": "ellipsis rank01"})
            singers = parse.find_all("div", {"class": "ellipsis rank02"})
            albums = parse.find_all("div", {"class": "ellipsis rank03"})
            albums_images = parse.find_all("a", {"class": "image_typeAll"})

            if titles and singers and albums and albums_images:
                return titles, singers, albums, albums_images
        except Exception as e:
            print(e)
        return [], [], [], []

    def numeric_genre_code(self):
        match = re.search(r'\d+', self.genre_code)
        if match:
            code = int(match.group())
            if code < 900:
                return 'Domestic'
            elif 1000 < code < 1500:
                return 'Oversea'
        return 'etc'

    def crawling_chart(self, target_count):
        title_list = []
        singer_list = []
        album_list = []
        album_images_list = []
        countries_list = []
        start_index = 1
        url_index = 0
        page = 1

        while len(title_list) < target_count:
            if page > self.pages:
                print("Maximum number of pages")
                break

            titles, singers, albums, albums_images = self.get_music_data(start_index, url_index)

            if not titles or not singers or not albums:
                url_index = 1
                start_index = 1
                continue

            for t in titles:
                title_list.append(t.find('a').text)

            for s in singers:
                singer_list.append(s.find('span', {"class": "checkEllipsis"}).text)
            for a in albums:
                album_list.append(a.find('a').text)
            for ai in albums_images[4:]:
                album_images_list.append(ai.find('img')['src'])
            for _ in range(target_count):
                countries_list.append(self.numeric_genre_code())

            start_index += 50
            page += 1

        return (title_list[:TARGET_COUNT], singer_list[:TARGET_COUNT],
                album_list[:TARGET_COUNT], album_images_list[:TARGET_COUNT], countries_list[:TARGET_COUNT])

    def close(self):
        self.driver.close()


def update_all_genre():
    for genre, genre_code in genre_code_map.items():
        melon_crawler = MelonGenreList(genre_code, pages=50)
        titles, singers, albums, album_images, countries = melon_crawler.crawling_chart(TARGET_COUNT)
        model = crawling_genre_model[genre]
        model.objects.all().delete()
        melon_crawler.close()

        chart_entries = []
        for i in range(TARGET_COUNT):
            entry = model(rank=i + 1, title=titles[i], singer=singers[i],
                          album=albums[i], album_image=album_images[i],country=countries[i])
            chart_entries.append(entry)

        model.objects.bulk_create(chart_entries)