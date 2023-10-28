from django.shortcuts import render
from django.views.generic import ListView
from .models import Chat, Message


class ChatList(ListView):
    model = Chat


def chat_create(request, uuid):
    pass