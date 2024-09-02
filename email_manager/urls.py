from django.urls import path
from .views import message_list, fetch_emails_view, email_progress

urlpatterns = [
    path('messages/', message_list, name='message_list'),
    path('fetch-emails/', fetch_emails_view, name='fetch_emails'),
    path('email-progress/', email_progress, name='email_progress'),
]
