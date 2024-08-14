import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from ai.DL.data_preprocessing import preprocess_data  # 데이터 전처리 파일에서 가져옴

pd.set_option('display.max_columns', None)  # 모든 열을 출력
pd.set_option('display.width', None)  # 출력될 DataFrame의 너비를 제한하지 않음


# 1. 모델 로드 함수
def load_model_and_scaler(model_path, scaler_path):
    def triplet_loss(y_true, y_pred, alpha=0.2):
        anchor, positive, negative = y_pred[:, 0], y_pred[:, 1], y_pred[:, 2]

        pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
        neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)

        loss = tf.maximum(pos_dist - neg_dist + alpha, 0.0)
        return tf.reduce_mean(loss)

    # 전체 모델(triplet model) 로드
    loaded_model = tf.keras.models.load_model(model_path, custom_objects={'triplet_loss': triplet_loss})

    # 스케일러 로드
    scaler_params = np.load(scaler_path)
    loaded_scaler = StandardScaler()
    loaded_scaler.mean_ = scaler_params['mean_']
    loaded_scaler.scale_ = scaler_params['scale_']

    return loaded_model, loaded_scaler


# 2. 데이터 로드 및 전처리
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
directory = os.path.join(BASE_DIR, 'genre_audio_feature')
data, scaled_features, labels, _ = preprocess_data(directory)


# 3. 사용자가 입력한 여러 오디오 피처의 평균 임베딩을 계산하고 가장 가까운 곡 추천
def recommend_songs(user_audio_features_list, embedding_model, scaler, data, scaled_features):

    scaled_user_features = scaler.transform(user_audio_features_list)
    user_embeddings = embedding_model.predict(scaled_user_features)
    avg_user_embedding = np.mean(user_embeddings, axis=0)
    song_embeddings = embedding_model.predict(scaled_features)
    distances = np.linalg.norm(song_embeddings - avg_user_embedding, axis=1)
    recommended_indices = np.argsort(distances)

    recommended_songs = data.iloc[recommended_indices][
        ['title', 'artist', 'album_image', 'track_id', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
         'instrumentalness', 'liveness', 'valence', 'tempo', 'genre']]
    recommended_songs = recommended_songs.drop_duplicates(subset=['track_id']).head(50)

    return recommended_songs



def load_and_use_model(user_audio_features_list):
    model_path = os.path.join(BASE_DIR, 'DL/Model/advance/triplet_model_advance.keras')
    scaler_path = os.path.join(BASE_DIR, 'DL/Model/advance/scaler_params.npz')
    base_network_path = os.path.join(BASE_DIR, 'DL/Model/advance/base_network_advance.keras')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    if not os.path.exists(base_network_path):
        raise FileNotFoundError(f"Base network file not found: {base_network_path}")

    # 모델 및 스케일러 로드
    loaded_model, loaded_scaler = load_model_and_scaler(model_path, scaler_path)

    # 베이스 네트워크 로드
    embedding_model = tf.keras.models.load_model(base_network_path)

    # 추천 시스템 실행
    recommended_songs = recommend_songs(user_audio_features_list, embedding_model, loaded_scaler, data, scaled_features)

    return recommended_songs
