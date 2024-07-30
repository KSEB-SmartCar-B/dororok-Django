from bs4 import BeautifulSoup
import requests

from crawling.models import crawling_genre_model

RANK = 45
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
    def __init__(self, genre_code):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        url = f'https://www.melon.com/genre/song_list.htm?gnrCode={genre_code}&steadyYn=Y'
        req = requests.get(url, headers=self.header)
        html = req.text
        self.parse = BeautifulSoup(html, "html.parser")

        self.titles = self.parse.find_all("div", {"class": "ellipsis rank01"})
        self.singers = self.parse.find_all("div", {"class": "ellipsis rank02"})
        self.albums = self.parse.find_all("div", {"class": "ellipsis rank03"})
        self.albums_images = self.parse.find_all("a", {"class": "image_typeAll"})

    def crawling_chart(self, rank):
        title = []
        singer = []
        album = []
        album_images = []

        for t in self.titles:
            title.append(t.find('a').text)

        for s in self.singers:
            singer.append(s.find('span', {"class": "checkEllipsis"}).text)
        for a in self.albums:
            album.append(a.find('a').text)
        for ai in self.albums_images:
            album_images.append(ai.find('img')['src'])

        return title[:rank], singer[:rank], album[:rank], album_images[:rank]


def update_all_genre():
    for genre, genre_code in genre_code_map.items():
        melon_crawler = MelonGenreList(genre_code)
        titles, singers, albums, album_images = melon_crawler.crawling_chart(RANK)
        model = crawling_genre_model[genre]
        model.objects.all().delete()

        chart_entries = []
        for i in range(RANK):
            entry = model(rank=i + 1, title=titles[i], singer=singers[i], album=albums[i], album_image=album_images[i])
            chart_entries.append(entry)

        model.objects.bulk_create(chart_entries)