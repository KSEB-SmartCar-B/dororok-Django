from django.db import models

# Create your models here.


class SeaCoordinate(models.Model):
    name = models.CharField(max_length=255)
    local_government = models.CharField(max_length=255)
    management_agency = models.CharField(max_length=255)
    beach_name = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class DororokFavoriteMusic(models.Model):
    favorite_music_id = models.IntegerField()
    artist = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    track_id = models.CharField(max_length=255)
    member_id = models.IntegerField()

    class Meta:
        db_table = 'favorites_music'
        managed = False


class DororokListeningMusic(models.Model):
    track_id = models.CharField(max_length=255)
    member_id = models.IntegerField()

    class Meta:
        db_table = 'music_listening_log'
        managed = False


class DororokFavoriteGenre(models.Model):
    genre_id = models.IntegerField()
    member_id = models.IntegerField()

    class Meta:
        db_table = 'favorite_genres'
        managed = False