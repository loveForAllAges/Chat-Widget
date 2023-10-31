from django.urls import path
from .views import *


urlpatterns = [
    path('', ChatList.as_view(), name='chat-list'),
    path('agent/', AgentList.as_view(), name='agent-list'),
    path('get-chat-data/', ChatAPIView.as_view(), name='get-chat-data'),
    path('<uuid:pk>/', ChatDetail.as_view(), name='chat-detail'),
]
