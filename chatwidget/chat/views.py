from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from .models import Chat, Message
from django.contrib.auth.models import User


class ChatList(ListView):
    model = Chat


class AgentList(ListView):
    model = User
    template_name = 'agent-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['chat_name'] = self.request.session.session_key
        return context


def chat_create(request, uuid):
    pass


def chat_delete(request, uuid):
    pass


def chat(request, uuid):
    pass
