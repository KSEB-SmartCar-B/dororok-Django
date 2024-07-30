import os
import django
from django.core.exceptions import ImproperlyConfigured
from spotify.authentication.spotify_auth import get_spotify_client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dororok-Django.config.settings')
django.setup()

try:
    from crawling.models import genre_models
except ImportError as e:
    raise ImproperlyConfigured(f"모델을 불러오는 중 오류 발생: {e}")

class SearchTrackId:
    def __init__(self):
        self.sp = get_spotify_client()

    def parse_track_id(self, titles, singers):
        track_ids = []
        for title, singer in zip(titles, singers):
            try:
                track_results = self.sp.search(q=f"track:{title} artist:{singer}", limit=1, type='track', market='KR')
                if track_results['tracks']['items']:
                    track_id = track_results['tracks']['items'][0]['id']
                    track_ids.append(track_id)
                else:
                    track_ids.append(None)
            except Exception as e:
                print(f"Error while searching for track {title} by {singer}: {e}")
                track_ids.append(None)
        return track_ids


def extract_before_parenthesis(input_str):
    pos = input_str.find('(')
    if pos != -1:
        return input_str[:pos]
    return input_str


def get_titles_and_singers_by_genre(genre):
    try:
        model_class = genre_models[genre]
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
    cnt = 1
    titles, singers = get_titles_and_singers_by_genre(genre)
    searcher = SearchTrackId()
    track_ids = searcher.parse_track_id(titles, singers)


    for title, singer, track_id in zip(titles, singers, track_ids):
        print(f"[{cnt}] 장르: {genre}, 제목: {title}, 가수: {singer}, 트랙 ID: {track_id}")
        cnt += 1

def search_all_genres():
    genres = ['댄스', '발라드', '인디', '트로트', 'OST',
               'POP', 'JPOP', '재즈', '클래식', '뉴에이지',
               '일렉트로니카', '국내 밴드', '해외 밴드',
               '국내 록메탈', '해외 록메탈', '국내 RBSOUL', '해외 RBSOUL',
               '국내 랩힙합', '해외 랩힙합', '국내 포크블루스', '해외 포크블루스컨트리']


    for genre in genres:
        print(f"Searching for genre: {genre}")
        search_and_print_track_ids(genre)

if __name__ == "__main__":
    search_all_genres()
