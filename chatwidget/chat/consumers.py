from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils.timesince import timesince
from asgiref.sync import sync_to_async
from .models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['pk']
        self.chat_group_name = f'chat_{self.chat_id}'
        
        await self.get_chat()
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        content = text_data_json['content']
        is_agent = text_data_json['is_agent']

        print('RECEIVE:', text_data_json)

        if type == 'message':
            new_message = await self.create_message(is_agent, content)

            await self.channel_layer.group_send(
                self.chat_group_name, {
                    'type': 'chat_message',
                    'content': content,
                    'is_agent': is_agent,
                    'created_at': timesince(new_message.created_at),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'content': event['content'],
            'created_at': event['created_at'],
        }))

    @sync_to_async
    def get_chat(self):
        self.chat = Chat.objects.get(pk=self.chat_id)

    @sync_to_async
    def create_message(self, is_agent, content):
        message = Message.objects.create(is_agent=is_agent, content=content)
        self.chat.messages.add(message)
        return message
