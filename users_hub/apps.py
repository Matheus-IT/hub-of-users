from django.apps import AppConfig


class UsersHubConfig(AppConfig):
    name = 'users_hub'

    def ready(self):
    	import users_hub.signals
