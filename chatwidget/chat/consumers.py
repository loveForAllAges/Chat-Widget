from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['pk']
        self.chat_group_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']
        
        await self.get_chat()
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

        if (self.user.is_staff or self.user.is_superuser) and not await self.check_client():
            await self.update_chat()
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_info',
                    'content': f'Менеджер {self.user.first_name} зашел в чат'
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        content = text_data_json['content']
        is_agent = text_data_json['is_agent']

        if type == 'message':
            new_message = await self.create_message(is_agent, content)
            await self.channel_layer.group_send(
                self.chat_group_name, {
                    'type': 'chat_message',
                    'content': content,
                    'is_agent': is_agent,
                    'created_at_formatted': new_message.created_at_formatted(),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'content': event['content'],
            'is_agent': event['is_agent'],
            'created_at_formatted': event['created_at_formatted'],
        }))

    async def chat_info(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_info',
            'content': event['content']
        }))

    @sync_to_async
    def get_chat(self):
        self.chat = Chat.objects.get(pk=self.chat_id)

    @sync_to_async
    def check_client(self):
        return self.chat == self.user.chat.first() or self.chat.agent

    @sync_to_async
    def update_chat(self):
        self.chat.status = 1
        self.chat.agent = self.user
        self.chat.save()

    @sync_to_async
    def create_message(self, is_agent, content):
        message = Message.objects.create(is_agent=is_agent, content=content)
        self.chat.messages.add(message)
        return message
