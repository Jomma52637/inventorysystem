from django.apps import AppConfig


class users(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals