from django.urls import path
from .views import *


urlpatterns = [
    path('', ChatList.as_view(), name='chat-list'),
    path('get-chat-data/', ChatAPIView.as_view(), name='get-chat-data'),
    # path('activate/', ActivateChatAPIView.as_view(), name='chat-activate'),
    path('<uuid:pk>/', ChatDetail.as_view(), name='chat-detail'),
    path('close/', ChatClose.as_view(), name='chat-close'),
]
