import pandas as pd
from recommendation.music_recommender.params.params import MusicRecommendationParams


def get_feature_weights(weather, time_of_day, precipitation):
    weather_weight = {
        "맑음": {"energy": 1.2, "danceability": 1.1, "valence": 1.2, "speechiness": 0.3, "acousticness": 0.1, "instrumentalness": 0.2},
        "흐림": {"energy": 0.2, "danceability": 0.3, "valence": 0.2, "speechiness": 0.9, "acousticness": 1.0, "instrumentalness": 1.0},
        "구름많음": {"energy": 0.4, "danceability": 0.4, "valence": 0.5, "speechiness": 0.8, "acousticness": 0.9, "instrumentalness": 0.8}
    }

    time_weight = {
        "6to12": {"tempo": 0.3, "energy": 0.4, "acousticness": 1.0, "speechiness": 1.2, "instrumentalness": 1.2},
        "12to18": {"tempo": 1.1, "energy": 1.3, "acousticness": 0.1, "speechiness": 0.3, "instrumentalness": 0.2},
        "18to24": {"tempo": 0.5, "energy": 0.6, "acousticness": 0.8, "speechiness": 0.7, "instrumentalness": 0.6},
        "24to6": {"tempo": 0.2, "energy": 0.2, "acousticness": 1.3, "speechiness": 1.3, "instrumentalness": 1.3}
    }

    precipitation_weight = {
        "없음": {"loudness": 1.2, "danceability": 1.0, "speechiness": 0.3, "acousticness": 0.2, "instrumentalness": 0.2},
        "비": {"loudness": 0.1, "danceability": 0.2, "speechiness": 1.2, "acousticness": 1.3, "instrumentalness": 1.3},
        "눈": {"loudness": 0.3, "danceability": 0.3, "speechiness": 1.0, "acousticness": 1.1, "instrumentalness": 1.1},
        "소나기": {"loudness": 0.4, "danceability": 0.5, "speechiness": 0.9, "acousticness": 0.9, "instrumentalness": 0.9}
    }

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

def dororok_recommendation(music_list, params):
    weather = params.sky_condition
    time_of_day = params.day_part
    precipitation = params.precipitation

    weights = get_feature_weights(weather, time_of_day, precipitation)

    for i, music in enumerate(music_list):
        try:
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
        except KeyError as e:
            return {"error": f"Missing expected feature: {str(e)} in music: {music}"}

    recommended_songs = sorted(music_list, key=lambda x: x.get('score', 0), reverse=True)[:30]
    print(recommended_songs)

    filtered_recommendations = []
    for music in recommended_songs:
        if isinstance(music, dict):
            filtered_recommendations.append({
                'title': music.get('title', ''),
                'artist': music.get('artist', ''),
                'track_id': music.get('track_id', ''),
                'album_image': music.get('album_image', '')
            })
        else:
            return {"error": f"Unexpected item type in recommended_songs: {type(music)}"}

    return filtered_recommendations
