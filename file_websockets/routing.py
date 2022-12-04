from django.urls import re_path

from .consumers import ReceiveFileConsumer

websocket_urlpatterns = [
    re_path(r'ws/files/(?P<session>\w+)/$', ReceiveFileConsumer.as_asgi()),
    re_path(r'ws/stream/files/(?P<session>\w+)/$', ReceiveFileConsumer.as_asgi()),
]