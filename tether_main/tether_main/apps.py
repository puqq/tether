# tether_main/apps.py
from django.apps import AppConfig

class TetherMainConfig(AppConfig):
    name = 'tether_main'
    def ready(self):
        import tether_main.signals
