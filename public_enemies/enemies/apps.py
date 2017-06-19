from django.apps import AppConfig


class EnemiesConfig(AppConfig):
    name = 'public_enemies.enemies'
    verbose_name = "Enemies"

    def ready(self):
        pass