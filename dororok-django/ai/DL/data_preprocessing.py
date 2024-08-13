import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_merge_csvs(directory, encoding='utf-8-sig'):
    """
    지정된 디렉토리 내의 모든 CSV 파일을 로드하여 병합합니다.
    """
    data_frames = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(directory, filename), encoding=encoding)
                data_frames.append(df)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
    merged_data = pd.concat(data_frames, ignore_index=True)
    return merged_data

def preprocess_data(directory, encoding='utf-8-sig'):
    """
    데이터를 로드하고 전처리(불필요한 열 제거 및 NaN 처리)한 후, 정규화된 피처를 반환합니다.
    """
    data = load_and_merge_csvs(directory, encoding=encoding)

    # 불필요한 열 제거, 장르와 필요한 피처만 남김
    columns_to_drop = ['title', 'artist', 'track_id', 'track_image', 'country', 'type', 'id', 'uri',
                       'track_href', 'analysis_url', 'duration_ms', 'time_signature']
    audio_features = data.drop(columns=columns_to_drop)

    audio_features = audio_features.dropna()

    labels = data['genre'].values  # 장르 정보 추출

    audio_features = audio_features.drop(columns=['genre'])
# NaN 값 제거
    audio_features = audio_features.dropna()
# 데이터 정규화
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(audio_features)

    return data, scaled_features, labels, scaler
