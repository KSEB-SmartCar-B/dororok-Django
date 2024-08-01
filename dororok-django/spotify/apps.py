from django.apps import AppConfig


class SpotifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spotify'

class SpotifyAppConfig(AppConfig):
    name = 'spotify'

    def ready(self):
        from .models import spotify_genre_model
        from django.db import models

        for model_name, model_class in spotify_genre_model.items():
            models.registry.register_model(self.name, model_class)