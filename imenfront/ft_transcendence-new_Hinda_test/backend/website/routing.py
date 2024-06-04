from django.urls import re_path
from . import consumers

# define the websocket url patterns
websocket_urlpatterns = [
    re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
]