from django.db import models

class BaseChartEntry(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    album_image = models.CharField(max_length=255)

    class Meta:
        abstract = True

def create_genre_model(genre_name):
    class Meta:
        db_table = f'{genre_name.upper()}'

    attrs = {
        '__module__': __name__,
        'Meta': Meta,
    }
    return type(f'{genre_name.upper()}Entry', (BaseChartEntry,), attrs)

genres = [    '댄스', '발라드', '인디', '트로트', 'OST',
              'POP', 'J-POP', '재즈', '클래식', '뉴에이지',
              '일렉트로니카', '국내 밴드', '해외 밴드',
              '국내 록메탈', '해외 록메탈',
              '국내 R&BSOUL', '해외 R&BSOUL',
              '국내 랩힙합', '해외 랩 힙합'
              '국내 포크블루스', '해외 포크블루스컨트리'  ]

genre_models = {
    genre:create_genre_model(genre) for genre in genres
}