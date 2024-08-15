import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from recommendation.music_recommender.genre_filter import genre_id_map
from recommendation.models import DororokFavoriteGenre


def audio_features_base_favorite_genre(member_id):
    user_genre_ids = DororokFavoriteGenre.objects.filter(member_id=member_id).values_list('genre_id', flat=True)
    user_genres = [genre_id_map[str(genre_id)] for genre_id in user_genre_ids if str(genre_id) in genre_id_map]

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    directory = os.path.join(BASE_DIR, 'ai/genre_audio_feature')

    data_frames = []

    for genre in user_genres:
        filename = f'{genre}_audio_feature.csv'
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):  # 파일 경로로 존재 여부 확인
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
                data_frames.append(df)
            except Exception as e:
                print(f"Error {file_path}: {e}")
                continue
    data = pd.concat(data_frames, ignore_index=True)

    columns_to_drop = ['title', 'artist', 'track_id', 'genre', 'album_image', 'country', 'type', 'id', 'uri',
                       'track_href', 'analysis_url', 'duration_ms', 'time_signature']
    data.drop(columns_to_drop, axis=1, inplace=True)
    audio_features_mean = data.mean()

    return audio_features_mean
