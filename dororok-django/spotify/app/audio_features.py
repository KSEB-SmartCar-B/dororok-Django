import os
import time
import django
import pandas as pd
import spotipy
from spotipy.exceptions import SpotifyException

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from spotify.authentication.spotify_auth import get_spotify_client
from spotify.models import spotify_genre_model


class AudioFeature:
    def __init__(self):
        self.sp = get_spotify_client()

    def track_feature(self, track_df):
        track_ids = track_df['track_id'].tolist()
        track_features = []
        batch_size = 100

        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            while True:
                try:
                    af = self.sp.audio_features(batch)
                    if af:
                        # None 값을 필터링
                        track_features.extend([feature for feature in af if feature is not None])
                    time.sleep(0.5)  # 각 요청 사이에 지연 시간 추가
                    break
                except SpotifyException as e:
                    if e.http_status == 429:
                        retry_after = int(e.headers.get('Retry-After', 5))  # 기본 5초 대기
                        print(f"Rate limited. Retrying after {retry_after} seconds.")
                        time.sleep(retry_after)
                    else:
                        print(f"Error fetching audio features for batch {batch}: {e}")
                        break
                except Exception as e:
                    print(f"Error fetching audio features for batch {batch}: {e}")
                    break

        if track_features:
            tf_df = pd.DataFrame(track_features)
            result_df = pd.concat([track_df.reset_index(drop=True), tf_df.reset_index(drop=True)], axis=1)
        else:
            result_df = track_df

        return result_df


def get_track_data_from_genre(genre):
    GenreModel = spotify_genre_model[genre]
    return GenreModel.objects.values_list('title', 'artist', 'track_id', 'track_image', 'country')


def save_genres_audio_feature(genre):
    audio_feature = AudioFeature()

    print(f"Processing genre: {genre}")
    track_data = get_track_data_from_genre(genre)
    track_df = pd.DataFrame(list(track_data), columns=['title', 'artist', 'track_id', 'track_image', 'country'])

    features_df = audio_feature.track_feature(track_df=track_df)
    directory = 'ai/genre_audio_feature'
    if not os.path.exists(directory):
        os.makedirs(directory)
    csv_file = os.path.join(directory, f'{genre}_audio_feature.csv')

    if os.path.exists(csv_file):
        os.remove(csv_file)
    try:
        features_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"File saved successfully to {csv_file}")
    except OSError as e:
        print(f"Error saving file: {e}")
    print(features_df.head())
