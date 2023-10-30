from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Chat, Message
from account.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework import views, response
from .serializers import ChatSerializer


class ChatList(ListView):
    model = Chat
    template_name = 'chat-list.html'


class AgentList(ListView):
    template_name = 'agent-list.html'

    def get_queryset(self):
        return User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_name'] = self.request.session.session_key
        return context


class ChatCreateView(View):
    def post(self, request):
        if request.user.is_authenticated:
            client_name = request.user.first_name
            client = request.user
        else:
            client_name = request.POST.get('content', 'Анонимный пользователь')
            client = None

        c = Chat.objects.create(client_name=client_name, client=client)

        return JsonResponse({'chat': 'success'})



def chat_delete(request, uuid):
    pass


def chat(request, uuid):
    pass


def get_chat_id(request):
    sk = request.session.session_key

    if sk:
        if request.user.is_authenticated:
            c, trash = Chat.objects.get_or_create(client=request.user)
        else:
            c, trash = Chat.objects.get_or_create(sk=sk)
    else:
        request.session['chat'] = []
        request.session.save()
        sk = request.session.session_key
        c = Chat.objects.create(sk=sk)

    return JsonResponse({'chatId': c.pk})


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
