import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from ai.DL.load_and_use_model import load_and_use_model
from recommendation.music_recommender.favorite_audio_feature import get_favorite_and_listen_tracks_audio_features, get_audio_features_for_tracks

def with_lover_or_friend(genre, member_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, f'../../ai/genre_audio_feature/{genre}_audio_feature.csv')
    df = pd.read_csv(file_path)

    features = df[['danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness',
                   'liveness', 'valence', 'tempo']]

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)

    favorite_features = get_favorite_and_listen_tracks_audio_features(member_id)

    favorite_features = scaler.transform(favorite_features)

    mean_scaled_features = scaled_features.mean(axis=0)

    initial_recommendations = load_and_use_model([mean_scaled_features])

    recommended_track_ids = initial_recommendations['track_id'].tolist()
    recommended_features = get_audio_features_for_tracks(recommended_track_ids)


    favorite_mean = favorite_features.mean(axis=0).reshape(1, -1)
    recommended_features = np.array(recommended_features)

    cosine_similarities = cosine_similarity(recommended_features, favorite_mean).flatten()

    sorted_indices = np.argsort(-cosine_similarities)

    top_indices = sorted_indices[:30]

    final_recommendations = []

    for idx in top_indices:
        track_id = recommended_track_ids[idx]
        track_info = initial_recommendations.loc[initial_recommendations['track_id'] == track_id].iloc[0]
        audio_features = recommended_features[idx]  # 오디오 피처

        final_recommendations.append({
            'title': track_info['title'],
            'artist': track_info['artist'],
            'album_image': track_info['album_image'],  # 이미지 URL
            'track_id': track_info['track_id'],
            'danceability': audio_features[0],
            'energy': audio_features[1],
            'key': audio_features[2],
            'loudness': audio_features[3],
            'mode': audio_features[4],
            'speechiness': audio_features[5],
            'acousticness': audio_features[6],
            'instrumentalness': audio_features[7],
            'liveness': audio_features[8],
            'valence': audio_features[9],
            'tempo': audio_features[10]
        })

    return final_recommendations
