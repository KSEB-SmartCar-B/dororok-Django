import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from ai.DL.load_and_use_model import load_and_use_model
from recommendation.music_recommender.favorite_audio_feature import get_favorite_and_listen_tracks_audio_features, get_audio_features_for_tracks

def with_lover_or_friend(genre, member_id):
    # CSV 파일에서 데이터 로드
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, f'../../ai/genre_audio_feature/{genre}_audio_feature.csv')
    df = pd.read_csv(file_path)

    # 오디오 피처 컬럼 선택 (필요한 컬럼만 지정)
    features = df[['danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness',
                   'liveness', 'valence', 'tempo']]

    # MinMaxScaler를 사용하여 모든 피처를 0과 1 사이로 변환
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)

    # 사용자 트랙의 오디오 피처 가져오기
    favorite_features = get_favorite_and_listen_tracks_audio_features(member_id)

    # favorite_features도 스케일링
    favorite_features = scaler.transform(favorite_features)

    # 평균 값 계산
    mean_scaled_features = scaled_features.mean(axis=0)

    # 1차 추천: scaled_features 기반
    initial_recommendations = load_and_use_model([mean_scaled_features])

    # 1차 추천 결과에서 추천된 트랙들의 오디오 피처 가져오기
    recommended_track_ids = initial_recommendations['track_id'].tolist()
    recommended_features = get_audio_features_for_tracks(recommended_track_ids)

    # 2차 추천: 1차 추천 결과와 favorite_features 기반
    refined_recommendations = []

    # favorite_features의 평균값과 1차 추천 트랙 피처 간 코사인 유사도 계산
    favorite_mean = favorite_features.mean(axis=0).reshape(1, -1)
    recommended_features = np.array(recommended_features)

    cosine_similarities = cosine_similarity(recommended_features, favorite_mean).flatten()

    # 유사도에 따라 정렬
    sorted_indices = np.argsort(-cosine_similarities)

    # 상위 N개의 추천 결과 선택
    top_indices = sorted_indices[:30]

    # 최종 추천 결과를 포함할 리스트
    final_recommendations = []

    for idx in top_indices:
        track_id = recommended_track_ids[idx]
        track_info = initial_recommendations.loc[initial_recommendations['track_id'] == track_id].iloc[0]
        audio_features = recommended_features[idx]  # 오디오 피처

        # 개별 오디오 피처를 분리하여 저장
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
