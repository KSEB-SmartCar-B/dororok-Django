from ai.DL.load_and_use_model import load_and_use_model
from recommendation.models import DororokFavoriteMusic, DororokListeningMusic
from spotify.authentication.spotify_auth import get_spotify_client


def get_audio_features_for_tracks(track_ids):
    sp = get_spotify_client()
    audio_features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i + 100]
        features = sp.audio_features(batch)
        for feature in features:
            if feature:
                audio_features.append([
                    feature['danceability'],
                    feature['energy'],
                    feature['key'],
                    feature['loudness'],
                    feature['mode'],
                    feature['speechiness'],
                    feature['acousticness'],
                    feature['instrumentalness'],
                    feature['liveness'],
                    feature['valence'],
                    feature['tempo']
                ])
    return audio_features


def get_favorite_and_listen_tracks_audio_features(member_id: int, favorite_weight: int = 3):
    # 좋아하는 트랙과 듣는 트랙을 가져오기
    favorite_tracks = DororokFavoriteMusic.objects.filter(member_id=member_id).values_list('track_id', flat=True)
    listen_tracks = DororokListeningMusic.objects.filter(member_id=member_id).values_list('track_id', flat=True)

    # 트랙 ID를 결합하고, 중복을 제거하기
    all_track_ids = list(set(favorite_tracks) | set(listen_tracks))

    # 각 트랙의 오디오 피처 가져오기
    audio_features = get_audio_features_for_tracks(all_track_ids)

    # 가중치를 부여하기 위해 favorite_tracks의 오디오 피처를 여러 번 추가
    favorite_audio_features = get_audio_features_for_tracks(favorite_tracks)
    for _ in range(favorite_weight - 1):
        audio_features.extend(favorite_audio_features)

    # 모델에 오디오 피처 전달하여 추천 받기
    return load_and_use_model(audio_features)



