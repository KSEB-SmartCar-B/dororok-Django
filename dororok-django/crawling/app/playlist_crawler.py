import os
import time

import django
from bs4 import BeautifulSoup
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from selenium import webdriver
from crawling.models import crawling_genre_model

TARGET_COUNT = 118

class MelonGenreList:
    def __init__(self, pages):
        self.pages = pages
        self.driver = webdriver.Chrome()  # 필요시 경로 추가
        # 예: self.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

    def get_music_data(self, start_index, url_index):
        urls = [
            #우정 f'https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=538334157'
            #사랑 f'https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=510267613'
            f'https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=525287420'
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
            print(f"Error occurred while fetching data: {e}")
        return [], [], [], []

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
                print("Maximum number of pages reached")
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
            for ai in albums_images:
                album_images_list.append(ai.find('img')['src'])
            for _ in range(len(titles)):
                countries_list.append('none')

            start_index += 50
            page += 1

        return (title_list[:TARGET_COUNT], singer_list[:TARGET_COUNT],
                album_list[:TARGET_COUNT], album_images_list[:TARGET_COUNT], countries_list[:TARGET_COUNT])

    def close(self):
        self.driver.close()


def update_all_genre():
    melon_crawler = MelonGenreList(pages=15)
    titles, singers, albums, album_images, countries = melon_crawler.crawling_chart(TARGET_COUNT)
    model = crawling_genre_model['바다']
    model.objects.all().delete()
    melon_crawler.close()

    chart_entries = []
    for i in range(TARGET_COUNT):
        entry = model(rank=i + 1, title=titles[i], singer=singers[i],
                      album=albums[i], album_image=album_images[i], country=countries[i])
        chart_entries.append(entry)

    model.objects.bulk_create(chart_entries)

if __name__ == '__main__':
    update_all_genre()
