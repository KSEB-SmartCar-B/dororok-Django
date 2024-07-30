from django.apps import AppConfig


class SpotifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spotify'

class SpotifyAppConfig(AppConfig):
    name = 'spotify'

    def ready(self):
        from .models import genre_models
        from django.db import models

        # 모델을 앱 레지스트리에 등록
        for model_name, model_class in genre_models.items():
            models.registry.register_model(self.name, model_class)