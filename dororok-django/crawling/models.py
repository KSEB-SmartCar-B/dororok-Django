from django.db import models


class BaseChartEntry(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=255)
    singer = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    album_image = models.CharField(max_length=255)
    country = models.CharField(max_length=100, default='etc')

    class Meta:
        abstract = True
        app_label = 'crawling'


def genre_model(genre_name):
    class Meta:
        db_table = f'{genre_name.upper()}'

    attrs = {
        '__module__': __name__,
        'Meta': Meta,
    }
    return type(f'{genre_name.upper()}Entry', (BaseChartEntry,), attrs)


class LastUpdate(models.Model):
    genre = models.CharField(max_length=50, unique=True)
    last_updated = models.DateTimeField(auto_now=True)


genres = ['댄스', '발라드', '인디', '트로트', 'OST',
          'POP', 'JPOP', '재즈', '클래식', '뉴에이지',
          '일렉트로니카', '국내 밴드', '해외 밴드',
          '국내 록메탈', '해외 록메탈', '국내 RBSOUL', '해외 RBSOUL',
          '국내 랩힙합', '해외 랩힙합', '국내 포크블루스', '해외 포크블루스컨트리']

crawling_genre_model = {
    genre: genre_model(genre) for genre in genres
}
