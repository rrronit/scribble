

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
from .models import Message
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
        await self.channel_layer.group_add(
                "all_together",
                self.channel_name
            )
        
        
        await self.accept()
 
       
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "all_together",
            self.channel_name
        )
   

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username =text_data_json["username"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        if message.strip() =="":
            return

        user =  await sync_to_async(User.objects.get,thread_sensitive=True)(username=username)
        pre_message = await sync_to_async(Message.objects.create,thread_sensitive=True)(user=user,content=message,timestamp=timestamp)
            
        await self.channel_layer.group_send(
            'all_together',
            {
                'type':'all_together',
                'message': message,
                'username': username,
                'timestamp': timestamp  
            }
        )

    async def all_together(self,event):
        data={
                'message': event['message'],
                'username': event['username'],
                'timestamp': event['timestamp']  
            }
   
        
        await self.send(text_data=json.dumps(
            data
        ))
 

