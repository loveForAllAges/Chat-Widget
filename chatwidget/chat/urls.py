from django.urls import path
from .views import *


urlpatterns = [
    path('chats/', ChatList.as_view(), name='chat-list'),
]
