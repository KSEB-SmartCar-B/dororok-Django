import os
import pandas as pd
from recommendation.models import DororokFavoriteGenre

genre_id_map = {
    '1': '댄스',
    '2': '발라드',
    '3': '인디',
    '4': '트로트',
    '5': 'OST',
    '6': 'POP',
    '7': 'JPOP',
    '8': '재즈',
    '9': '클래식',
    '10': '뉴에이지',
    '11': '일렉트로니카',
    '12': '국내 밴드',
    '13': '해외 밴드',
    '14': '국내 록메탈',
    '15': '해외 록메탈',
    '16': '국내 랩힙합',
    '17': '해외 랩힙합',
    '18': '국내 RBSOUL',
    '19': '해외 RBSOUL',
    '20': '국내 포크블루스',
    '21': '해외 포크블루스컨트리'
}


def filter_recommendations_by_genre(recommended_songs, member_id):
    # 사용자의 선호 장르 ID 가져오기
    user_genre_ids = DororokFavoriteGenre.objects.filter(member_id=member_id).values_list('genre_id', flat=True)

    # 장르 ID를 장르 이름으로 변환
    user_genres = [genre_id_map[str(genre_id)] for genre_id in user_genre_ids if str(genre_id) in genre_id_map]

    print(f"User Genre IDs: {user_genre_ids}")
    print(f"User Genres: {user_genres}")

    # 추천된 노래에서 사용자가 선호하는 장르만 필터링
    filtered_songs = recommended_songs[recommended_songs['genre'].isin(user_genres)]

    return filtered_songs


def save_recommendations_to_csv(recommended_songs, filtered_songs, member_id):
    # 파일 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    original_csv_path = os.path.join(base_dir, f"recommended_songs_{member_id}_original.csv")
    filtered_csv_path = os.path.join(base_dir, f"recommended_songs_{member_id}_filtered.csv")

    # 원래의 추천 결과를 CSV로 저장
    recommended_songs.to_csv(original_csv_path, index=False, encoding='utf-8-sig')

    # 필터링된 추천 결과를 CSV로 저장
    filtered_songs.to_csv(filtered_csv_path, index=False, encoding='utf-8-sig')
