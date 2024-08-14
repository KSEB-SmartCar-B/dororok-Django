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


def get_favorite_tracks(member_id: int, favorite_weight: int = 4):
    favorite_tracks = list(DororokFavoriteMusic.objects.filter(member_id=member_id).values_list('track_id', flat=True))
    favorite_audio_features = get_audio_features_for_tracks(favorite_tracks)

    weighted_audio_features = favorite_audio_features[:]
    for _ in range(favorite_weight - 1):
        weighted_audio_features.extend(favorite_audio_features)

    return weighted_audio_features


def get_listen_tracks(member_id: int):
    return list(DororokListeningMusic.objects.filter(member_id=member_id).values_list('track_id', flat=True))


def get_favorite_and_listen_tracks_audio_features(member_id: int):
    favorite_audio_features = get_favorite_tracks(member_id)
    listen_tracks = get_listen_tracks(member_id)

    all_track_ids = list(set(listen_tracks))

    audio_features = get_audio_features_for_tracks(all_track_ids)

    audio_features.extend(favorite_audio_features)

    return audio_features


def basic_recommendation_music(member_id: int):
    audio_features = get_favorite_and_listen_tracks_audio_features(member_id)
    return load_and_use_model(audio_features)
