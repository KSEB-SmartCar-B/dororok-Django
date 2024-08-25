
class SpotifyRouter:
    route_app_labels = {'spotify', 'crawling'}

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'spotify':
            return 'spotify_db'
        elif model._meta.app_label == 'crawling':
            return 'default'
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'spotify':
            return 'spotify_db'
        elif model._meta.app_label == 'crawling':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'spotify':
            return db == 'spotify_db'
        elif app_label == 'crawling':
            return db == 'default'
        return None


# routers.py

class SeaCoordinateRouter:
    """
    A router to control all database operations on SeaCoordinate models.
    """
    route_app_labels = {'recommendation'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read SeaCoordinate models go to sea_db.
        """
        if model._meta.app_label in self.route_app_labels and model._meta.model_name == 'seacoordinate':
            return 'sea_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write SeaCoordinate models go to sea_db.
        """
        if model._meta.app_label in self.route_app_labels and model._meta.model_name == 'seacoordinate':
            return 'sea_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a SeaCoordinate model is involved.
        """
        if (
                obj1._meta.model_name == 'seacoordinate' or
                obj2._meta.model_name == 'seacoordinate'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that SeaCoordinate models only appear in the 'sea_db'
        database.
        """
        if app_label in self.route_app_labels and model_name == 'seacoordinate':
            return db == 'sea_db'
        return None


class DororokRouter:
    """
    A router to control all database operations on Dororok-related models.
    """
    route_app_labels = {'recommendation'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read Dororok-related models go to dororok_db.
        """
        if model._meta.app_label in self.route_app_labels and model._meta.model_name in ['dororokfavoritemusic',
                                                                                         'dororoklisteningmusic',
                                                                                         'dororokfavoritegenre',
                                                                                         'dororokdestination',
                                                                                         'trackrecommendationhistory']:
            return 'dororok_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write Dororok-related models go to dororok_db.
        """
        if model._meta.app_label in self.route_app_labels and model._meta.model_name in ['dororokfavoritemusic',
                                                                                         'dororoklisteningmusic',
                                                                                         'dororokfavoritegenre',
                                                                                         'dororokdestination',
                                                                                         'trackrecommendationhistory']:
            return 'dororok_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a Dororok-related model is involved.
        """
        if (
                obj1._meta.model_name in ['dororokfavoritemusic', 'dororoklisteningmusic', 'dororokfavoritegenre', 'dororokdestination', 'trackrecommendationhistory'] or
                obj2._meta.model_name in ['dororokfavoritemusic', 'dororoklisteningmusic', 'dororokfavoritegenre', 'dororokdestination', 'trackrecommendationhistory']
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that Dororok-related models only appear in the 'dororok_db'
        database.
        """
        if app_label in self.route_app_labels and model_name in ['dororokfavoritemusic',
                                                                 'dororoklisteningmusic',
                                                                 'dororokfavoritegenre',
                                                                 'dororokdestination',
                                                                 'trackrecommendationhistory']:
            return db == 'dororok_db'
        return None

