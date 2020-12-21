from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/hub/', consumers.UsersHubConsumer.as_asgi())
]
