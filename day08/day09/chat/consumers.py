from collections import deque
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

chat_history = {}  
connected_users = {}

class chatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        user = self.scope["user"]
        if user.is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
            
            current_users = list(connected_users.get(self.room_group_name, []))
            self.send(json.dumps({
                "type":"user_list",
                "users": current_users}
            ))
            connected_users.setdefault(self.room_group_name, set()).add(user.username)
            async_to_sync(self.channel_layer.group_send)(self.room_group_name,
            {
                "type":"user_join",
                "username":user.username
            }
            )

            history = chat_history.get(self.room_group_name, [])
            for event in history:
                self.send(text_data=json.dumps(event))
            join_event = {
                "type": "server_message",
                "username": user.username,
                "message": f"{user.username} has joined the chat",
            }
            self._store_event(join_event)
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            join_event
        )
        else:
            self.close() 

    def receive(self, text_data = None, bytes_data = None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_event =     {
                'type':'chat_message',
                'username': self.scope["user"].get_username(),
                'message':message
            }
        self._store_event(message_event)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            message_event
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type':'chat',
            'username': event['username'],
            'message': message
        }))

    def server_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type':'server',
            'username': event['username'],
            'message': message
        }))

    def disconnect(self, close_code):
        connected_users[self.room_group_name].discard(self.scope["user"].username)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,
        {
            "type":"user_leave",
            "username":self.scope["user"].username
        }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def user_join(self, event):
        self.send(text_data=json.dumps({
            "type": "user_join",
            "username": event["username"]
        }))
    
    def user_leave(self, event):
        self.send(text_data=json.dumps({
            "type": "user_leave",
            "username": event["username"]
        }))

    def _store_event(self, event):
        """Store the last 3 messages per room"""
        room_history = chat_history.setdefault(self.room_group_name, deque(maxlen=3))
        room_history.append({
            "type": f"{'chat' if event['type'] == 'chat_message' else 'server'}",
            "username": event["username"],
            "message": event["message"]
        })