# -*- coding: utf-8 -*-
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from accounts.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data.get('user_id')
        
        if not user_id:
            return
        
        # Сохраняем сообщение в базу данных
        saved_message = await self.save_message(user_id, message)
        
        # Отправляем сообщение всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': saved_message['username'],
                'user_id': user_id,
                'timestamp': saved_message['timestamp']
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp']
        }))
    
    @database_sync_to_async
    def save_message(self, user_id, content):
        user = CustomUser.objects.get(id=user_id)
        message = Message.objects.create(user=user, content=content)
        return {
            'username': user.get_full_name() or user.username,
            'timestamp': message.timestamp.isoformat()
        }
