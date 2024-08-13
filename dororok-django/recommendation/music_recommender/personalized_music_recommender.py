import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recommendation.music_recommender.favorite_audio_feature import get_favorite_and_listen_tracks_audio_features
from recommendation.music_recommender.params.params import MusicRecommendationParams
from recommendation.music_recommender.genre_filter import filter_recommendations_by_genre, save_recommendations_to_csv


def recommend_music(params: MusicRecommendationParams):
    mode_to_function = {
        'daily': recommend_daily_music,
        'to_work': recommend_to_work_music,
        'leave_work': recommend_leave_work_music,
        'travel': recommend_travel_music,
        'drive': recommend_drive_music,
        'dororok': recommend_dororok_music,
        'with_lover': recommend_with_lover_music,
        'with_friends': recommend_with_friends_music,
    }
    if params.music_mode in mode_to_function:
        return mode_to_function[params.music_mode](params)
    else:
        return handle_invalid_mode(params.music_mode)


def get_recommendation_list(member_id: int):
    recommendation_music_list = []
    recommendation_music_list = get_favorite_and_listen_tracks_audio_features(member_id)

    filtered_list = filter_recommendations_by_genre(recommendation_music_list, member_id)
    save_recommendations_to_csv(recommendation_music_list, filtered_list, member_id)

if __name__ == '__main__':
    get_recommendation_list(2)

def recommend_daily_music(params: MusicRecommendationParams):

    return "Recommended daily music"


def recommend_to_work_music(params: MusicRecommendationParams):
    return "Recommended to-work music"


def recommend_leave_work_music(params: MusicRecommendationParams):
    return "Recommended leave-work music"


def recommend_travel_music(params: MusicRecommendationParams):
    return "Recommended travel music"


def recommend_drive_music(params: MusicRecommendationParams):
    return "Recommended drive music"


def recommend_dororok_music(params: MusicRecommendationParams):
    return "Recommended dororok music"


def recommend_with_lover_music(params: MusicRecommendationParams):
    return "Recommended with-lover music"


def recommend_with_friends_music(params: MusicRecommendationParams):
    return "Recommended with-friends music"


def handle_invalid_mode(music_mode):
    return f"Error: Invalid music mode '{music_mode}'"
