import os
import django
import numpy as np
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recommendation.music_recommender.favorite_audio_feature import basic_recommendation_music
from recommendation.music_recommender.params.params import MusicRecommendationParams
from recommendation.music_recommender.genre_filter import filter_recommendations_by_genre
from recommendation.geo_utils.is_near_sea import nearby_sea
from recommendation.music_recommender.sea_love_friendship import with_lover_or_friend


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
    recommendation_music_list = basic_recommendation_music(member_id)
    return recommendation_music_list


#추천 그대로
def recommend_daily_music(params: MusicRecommendationParams):
    daily_list = filter_recommendations_by_genre(get_recommendation_list(params.member_id), params.member_id)
    filtered_recommendations = daily_list[['title', 'artist', 'track_id', 'album_image']].to_dict(orient='records')
    return filtered_recommendations


#enery 높은 순서
def recommend_to_work_music(params: MusicRecommendationParams):
    work_list = filter_recommendations_by_genre(get_recommendation_list(params.member_id), params.member_id)
    filtered_recommendations = work_list[['title', 'artist', 'track_id', 'album_image']].to_dict(orient='records')
    return filtered_recommendations


#valance 높은 순서
def recommend_leave_work_music(params: MusicRecommendationParams):
    leave_work_list = filter_recommendations_by_genre(get_recommendation_list(params.member_id), params.member_id)
    filtered_recommendations = leave_work_list[['title', 'artist', 'track_id', 'album_image']].to_dict(orient='records')
    return filtered_recommendations


#바다, energy, valance, dancebility 평균 높은 것
#위치가 바다면 바다로 학습하고, 높은 거
#위치가 바다가 아니면 높은 거
def recommend_travel_music(params: MusicRecommendationParams):
    if nearby_sea(params.region1depth_name, params.lat, params.lng):
        travel_music = with_lover_or_friend("바다", params.member_id)
    else:
        travel_music = get_recommendation_list(params.member_id)

    if isinstance(travel_music, list):
        travel_music = pd.DataFrame(travel_music)
    travel_music['average_score'] = travel_music[['energy', 'valence', 'danceability']].mean(axis=1)
    drive_recommended_songs = travel_music.sort_values(by='average_score', ascending=False)
    filtered_recommendations = drive_recommended_songs[['title', 'artist', 'track_id', 'album_image']].to_dict(orient='records')

    return filtered_recommendations

#바다, tempo, energy, dancebility 높은 것
#위치가 바다면 바다로 학습하고, 높은 거
#위치가 바다가 아니면 높은 거
def recommend_drive_music(params: MusicRecommendationParams):
    if nearby_sea(params.region1depth_name, params.lat, params.lng):
        drive_music = with_lover_or_friend("바다", params.member_id)
    else:
        drive_music = get_recommendation_list(params.member_id)
    if isinstance(drive_music, list):
        drive_music = pd.DataFrame(drive_music)

    drive_music['average_score'] = drive_music[['tempo', 'energy', 'danceability']].mean(axis=1)
    drive_recommended_songs = drive_music.sort_values(by='average_score', ascending=False)
    filtered_recommendations = drive_recommended_songs[['title', 'artist', 'track_id', 'album_image']].to_dict(orient='records')
    return filtered_recommendations


#바다, 날씨, 시간, 강수, 하늘 상태
def recommend_dororok_music(params: MusicRecommendationParams):
    return "Recommended dororok music"


#달달한 노래 모델 학습, 달달한 노래 평균값을 input
def recommend_with_lover_music(params: MusicRecommendationParams):
    return with_lover_or_friend("사랑", params.member_id)


#우정 플리 모델 학습, 우정 플리 평균값 input
def recommend_with_friends_music(params: MusicRecommendationParams):
    return with_lover_or_friend("우정", params.member_id)


def handle_invalid_mode(music_mode):
    return f"Error: Invalid music mode '{music_mode}'"
