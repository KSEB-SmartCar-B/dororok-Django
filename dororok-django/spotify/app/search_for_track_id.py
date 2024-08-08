import os
import time
import django
import spotipy
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.exceptions import ImproperlyConfigured
from spotify.authentication.spotify_auth import get_spotify_client
from spotify.app.audio_features import save_genres_audio_feature
from spotify.models import genres

try:
    from crawling.models import crawling_genre_model, BaseChartEntry
    from spotify.models import spotify_genre_model
except ImportError as e:
    raise ImproperlyConfigured(f"모델을 불러오는 중 오류 발생: {e}")


class SearchTrackId:
    def __init__(self):
        self.sp = get_spotify_client()

    def parse_track_id(self, titles, singers):
        track_ids = []
        batch_size = 50
        max_batches = 10  # 최대 5번의 배치 처리

        for i in range(0, min(len(titles), batch_size * max_batches), batch_size):
            batch_titles = titles[i:i + batch_size]
            batch_singers = singers[i:i + batch_size]
            for title, singer in zip(batch_titles, batch_singers):
                try:
                    track_results = self.sp.search(q=f"track:{title} artist:{singer}", limit=1, type='track', market='KR')
                    if track_results['tracks']['items']:
                        track_id = track_results['tracks']['items'][0]['id']
                        track_ids.append(track_id)
                    else:
                        track_ids.append(None)
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Error while searching for track {title} by {singer}: {e}")
                    track_ids.append(None)
                    if isinstance(e, spotipy.exceptions.SpotifyException) and e.http_status == 429:
                        retry_after = int(e.headers.get('Retry-After', 1))
                        print(f"Rate limited. Retrying after {retry_after} seconds.")
                        time.sleep(retry_after)

        return track_ids


def extract_before_parenthesis(input_str):
    pos = input_str.find('(')
    if pos != -1:
        return input_str[:pos]
    return input_str


def get_titles_and_singers_by_genre(genre):
    try:
        model_class = crawling_genre_model[genre]
    except KeyError:
        raise ImproperlyConfigured(f"장르 '{genre}'에 대한 모델을 찾을 수 없습니다.")

    entries = model_class.objects.all()
    titles = [extract_before_parenthesis(entry.title) for entry in entries]
    if genre == '클래식':
        singers = ['클래식' for _ in entries]
    else:
        singers = [extract_before_parenthesis(entry.singer) for entry in entries]
    return titles, singers


def search_and_print_track_ids(genre):
    titles, singers = get_titles_and_singers_by_genre(genre)
    searcher = SearchTrackId()
    track_ids = searcher.parse_track_id(titles, singers)

    genre_model = spotify_genre_model[genre]
    chart_model = crawling_genre_model[genre]

    genre_model.objects.all().delete()

    entries_to_create = []
    for title, singer, track_id in zip(titles, singers, track_ids):
        if track_id is not None:
            track_image = 'photo/logo.png'
            country = 'etc'
            try:
                music_entry = chart_model.objects.filter(title__icontains=title, singer__icontains=singer).first()
                if music_entry:
                    track_image = music_entry.album_image
                    country = music_entry.country
                else:
                    print(f"Music entry for title '{title}' not found.")
            except chart_model.DoesNotExist:
                print(f"Music entry for title '{title}' not found.")

            entries_to_create.append(
                genre_model(
                    title=title,
                    artist=singer,
                    track_id=track_id,
                    track_image=track_image,
                    country=country
                )
            )

    if entries_to_create:
        genre_model.objects.bulk_create(entries_to_create)

    save_genres_audio_feature(genre)


def search_all_genres():
    all_genres = genres
    for genre in all_genres:
        print(f"Searching for genre: {genre}")
        search_and_print_track_ids(genre)


if __name__ == '__main__':
    search_all_genres()
