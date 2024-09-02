from django.urls import path
from email_manager.consumers import EmailProgressConsumer

websocket_urlpatterns = [
    path('ws/progress/', EmailProgressConsumer.as_asgi()),
]
