from django.apps import AppConfig


class NewspaperappConfig(AppConfig):
    name = 'NewsPaperApp'

    def ready(self):
        import NewsPaperApp.signals

