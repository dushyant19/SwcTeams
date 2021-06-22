from django.urls import re_path

from .consumers import BuildConsumer

websocket_urlpatterns = [
    re_path(r'ws/build/(?P<build_id>\w+)/$', BuildConsumer.as_asgi()),
]