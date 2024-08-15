from django.db import models


class BaseGenreSpotify(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    track_id = models.CharField(max_length=255)
    track_image = models.CharField(max_length=255, default='default.jpg')
    country = models.CharField(max_length=255, default='etc')

    class Meta:
        abstract = True
        app_label = 'spotify'


def spotify_genre(genre_name):
    class Meta:
        db_table = f'{genre_name.upper()}_entry'

    attrs = {
        '__module__': __name__,
        'Meta': Meta,
        'objects': models.Manager(),
    }
    return type(f'{genre_name.upper()}Entry', (BaseGenreSpotify,), attrs)


genres = [
    '댄스', '발라드', '인디', '트로트', 'OST',
    'POP', 'JPOP', '재즈', '클래식',
    '뉴에이지',
    '일렉트로니카', '국내 밴드', '해외 밴드',
    '국내 록메탈', '해외 록메탈', '국내 RBSOUL', '해외 RBSOUL',
    '국내 랩힙합', '해외 랩힙합', '국내 포크블루스', '해외 포크블루스컨트리',
#    '사랑', '우정', '바다'
]

# Dynamically create genre models
spotify_genre_model = {
    genre: spotify_genre(genre) for genre in genres
}