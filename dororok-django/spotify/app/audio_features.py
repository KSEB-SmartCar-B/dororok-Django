import os
import django
import pandas as pd

# Django 설정을 초기화합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from spotify.authentication.spotify_auth import get_spotify_client
from spotify.models import spotify_genre_model

class AudioFeature:
    def __init__(self):
        self.sp = get_spotify_client()

    def track_feature(self, track_df):
        track_features = []
        for t_id in track_df['track_id']:
            af = self.sp.audio_features(t_id)
            if af:
                track_features.extend(af)

        tf_df = pd.DataFrame(track_features, columns=[
            'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
            'time_signature'
        ])

        result_df = pd.concat([track_df.reset_index(drop=True), tf_df.reset_index(drop=True)], axis=1)
        return result_df

def get_track_data_from_genre(genre):
    GenreModel = spotify_genre_model[genre]
    return GenreModel.objects.values_list('title', 'track_id')

def save_genres_audio_feature(genre):

    audio_feature = AudioFeature()

    print(f"Processing genre: {genre}")
    track_data = get_track_data_from_genre(genre)
    track_df = pd.DataFrame(list(track_data), columns=['title', 'track_id'])

    features_df = audio_feature.track_feature(track_df=track_df)
    directory = '../../ai/genre_audio_feature'
    if not os.path.exists(directory):
        os.makedirs(directory)
    excel_file = os.path.join(directory, f'{genre}_audio_feature.csv')

    if os.path.exists(excel_file):
        os.remove(excel_file)
    try:
        features_df.to_csv(excel_file, index=False, encoding='utf-8-sig')
        print(f"File saved successfully to {excel_file}")
    except OSError as e:
        print(f"Error saving file: {e}")
    print(features_df.head())


if __name__ == "__main__":
    save_genres_audio_feature()
