from django.apps import AppConfig


class IlesConfig(AppConfig):
    name = 'ILES'
    #after adding signals
    def ready(self):
        import ILES.signals
