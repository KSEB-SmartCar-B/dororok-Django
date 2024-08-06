import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

#genres = ['POP', '발라드']
genres = [
    '댄스', '발라드', '인디', '트로트', 'OST',
    'POP', 'JPOP', '재즈', '클래식', '뉴에이지',
    '일렉트로니카', '국내 밴드', '해외 밴드',
    '국내 록메탈', '해외 록메탈', '국내 RBSOUL', '해외 RBSOUL',
    '국내 랩힙합', '해외 랩힙합', '국내 포크블루스', '해외 포크블루스컨트리'
]

features = [
    'danceability', 'energy', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo'
]


def plot_radar_chart(df, features, genre):
    df_normalized = df.copy()
    for feature in features:
        df_normalized[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())

    values = df_normalized[features].mean().tolist()

    values += values[:1]

    num_vars = len(features)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(features)

    plt.title(f'{genre} Normalized Average Audio Features')

    file_path = f'ai/genre_feature_chart/{genre}_radar_chart.png'

    if os.path.exists(file_path):
        os.remove(file_path)

    plt.savefig(file_path)
    plt.close()


def analyze_data():
    for genre in genres:
        csv_file_path = f'ai/genre_audio_feature/{genre}_audio_feature.csv'
        df = pd.read_csv(csv_file_path)
        plot_radar_chart(df, features, genre)


if __name__ == '__main__':
    analyze_data()