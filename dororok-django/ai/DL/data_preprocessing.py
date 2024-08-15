import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_merge_csvs(directory, encoding='utf-8-sig'):
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
    data = load_and_merge_csvs(directory, encoding=encoding)
    columns_to_drop = ['title', 'artist', 'track_id', 'album_image', 'country', 'type', 'id', 'uri',
                       'track_href', 'analysis_url', 'duration_ms', 'time_signature']
    audio_features = data.drop(columns=columns_to_drop)

    audio_features = audio_features.dropna()

    labels = data['genre'].values

    audio_features = audio_features.drop(columns=['genre'])
    audio_features = audio_features.dropna()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(audio_features)

    return data, scaled_features, labels, scaler
