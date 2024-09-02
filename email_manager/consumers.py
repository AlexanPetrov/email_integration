# email_manager/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class EmailProgressConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "email_progress",  
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "email_progress",  
            self.channel_name
        )

    def receive(self, text_data):
        pass  # No need to handle receive if only sending updates

    def send_progress_update(self, event):
        progress = event["progress"]
        self.send(text_data=json.dumps({
            'progress': progress
        }))
