import pandas as pd
from recommendation.music_recommender.params.params import MusicRecommendationParams

# 가중치 설정 함수
def get_feature_weights(weather, time_of_day, precipitation):
    weather_weight = {
        "맑음": {"energy": 0.8, "danceability": 0.7, "valence": 0.9, "speechiness": 0.5, "acousticness": 0.3, "instrumentalness": 0.4},
        "흐림": {"energy": 0.4, "danceability": 0.5, "valence": 0.4, "speechiness": 0.7, "acousticness": 0.6, "instrumentalness": 0.7},
        "구름 많음": {"energy": 0.5, "danceability": 0.4, "valence": 0.5, "speechiness": 0.6, "acousticness": 0.7, "instrumentalness": 0.6}
    }

    time_weight = {
        "6to12": {"tempo": 0.5, "energy": 0.5, "acousticness": 0.6, "speechiness": 0.7, "instrumentalness": 0.7},
        "12to18": {"tempo": 0.8, "energy": 0.9, "acousticness": 0.3, "speechiness": 0.6, "instrumentalness": 0.4},
        "18to24": {"tempo": 0.6, "energy": 0.7, "acousticness": 0.6, "speechiness": 0.5, "instrumentalness": 0.5},
        "24to6": {"tempo": 0.4, "energy": 0.4, "acousticness": 0.8, "speechiness": 0.8, "instrumentalness": 0.8}
    }

    precipitation_weight = {
        "없음": {"loudness": 0.8, "danceability": 0.7, "speechiness": 0.5, "acousticness": 0.4, "instrumentalness": 0.4},
        "비": {"loudness": 0.3, "danceability": 0.4, "speechiness": 0.7, "acousticness": 0.8, "instrumentalness": 0.8},
        "눈": {"loudness": 0.4, "danceability": 0.3, "speechiness": 0.6, "acousticness": 0.8, "instrumentalness": 0.7},
        "소나기": {"loudness": 0.5, "danceability": 0.6, "speechiness": 0.6, "acousticness": 0.5, "instrumentalness": 0.5}
    }

    # 가중치 통합
    combined_weights = {
        "energy": weather_weight[weather]['energy'] * time_weight[time_of_day]['energy'],
        "danceability": weather_weight[weather]['danceability'] * precipitation_weight[precipitation]['danceability'],
        "valence": weather_weight[weather]['valence'],
        "tempo": time_weight[time_of_day]['tempo'],
        "loudness": precipitation_weight[precipitation]['loudness'],
        "speechiness": weather_weight[weather]['speechiness'] * time_weight[time_of_day]['speechiness'] * precipitation_weight[precipitation]['speechiness'],
        "acousticness": weather_weight[weather]['acousticness'] * time_weight[time_of_day]['acousticness'] * precipitation_weight[precipitation]['acousticness'],
        "instrumentalness": weather_weight[weather]['instrumentalness'] * time_weight[time_of_day]['instrumentalness'] * precipitation_weight[precipitation]['instrumentalness']
    }

    return combined_weights

# 추천 알고리즘 구현
def dororok_recommendation(music_list, params):
    weather = params.sky_condition
    time_of_day = params.day_part
    precipitation = params.precipitation

    # 피처 가중치 계산
    weights = get_feature_weights(weather, time_of_day, precipitation)

    # 점수 계산
    for music in music_list:
        music['score'] = (
                music['energy'] * weights['energy'] +
                music['danceability'] * weights['danceability'] +
                music['valence'] * weights['valence'] +
                music['tempo'] * weights['tempo'] +
                music['loudness'] * weights['loudness'] +
                music['speechiness'] * weights['speechiness'] +
                music['acousticness'] * weights['acousticness'] +
                music['instrumentalness'] * weights['instrumentalness']
        )

    # 점수 기준으로 내림차순 정렬하여 상위 10곡 추천
    recommended_songs = sorted(music_list, key=lambda x: x['score'], reverse=True)[:10]

    # 필요한 필드만 포함된 결과 리스트 반환
    filtered_recommendations = [
        {
            'title': music['title'],
            'artist': music['artist'],
            'track_id': music['track_id'],
            'album_image': music['album_image']
        }
        for music in recommended_songs
    ]

    return filtered_recommendations
