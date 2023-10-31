from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Chat, Message
from account.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework import views, response
from .serializers import ChatSerializer
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.db.models import Count


class StaffOnly(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool | None:
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True
        raise Http404
    

class ChatList(StaffOnly, ListView):
    template_name = 'chat-list.html'
    queryset = Chat.objects.annotate(num_messages=Count('messages')).filter(num_messages__gt=0).order_by('-created_at')


class AgentList(StaffOnly, ListView):
    template_name = 'agent-list.html'

    def get_queryset(self):
        return User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_name'] = self.request.session.session_key
        return context


class ChatAPIView(views.APIView):
    def post(self, request):
        sk = request.session.session_key

        if sk:
            if request.user.is_authenticated:
                data, trash = Chat.objects.get_or_create(client=request.user)
            else:
                data, trash = Chat.objects.get_or_create(sk=sk)
        else:
            request.session['chat'] = []
            request.session.save()
            sk = request.session.session_key
            data = Chat.objects.create(sk=sk)

        serializer = ChatSerializer(data)
        return response.Response(serializer.data)


class ChatDetail(StaffOnly, DetailView):
    model = Chat
    template_name = 'agent-chat.html'
