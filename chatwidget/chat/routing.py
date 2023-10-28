from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/<uuid:pk>', consumers.ChatConsumer.as_asgi()),
]