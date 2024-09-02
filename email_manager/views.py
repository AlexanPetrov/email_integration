from django.shortcuts import render
from django.http import JsonResponse
from .models import EmailCredential, EmailMessage
from imapclient import IMAPClient
import email
import os
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def fetch_emails_view(request):
    total_emails_checked = 0  # Track number of checked emails
    credentials = EmailCredential.objects.all()
    for credential in credentials:
        try:
            # Determine the IMAP server based on the email domain
            if "gmail.com" in credential.email:
                imap_server = "imap.gmail.com"
            elif "yandex.ru" in credential.email:
                imap_server = "imap.yandex.ru"
            elif "mail.ru" in credential.email:
                imap_server = "imap.mail.ru"
            else:
                continue  # Skip if the email provider is not supported

            with IMAPClient(imap_server, use_uid=True) as server:
                server.login(credential.email, credential.password)
                server.select_folder('INBOX')
                messages = server.search(['NOT', 'DELETED'])
                total_emails = len(messages)
                for msg_id, data in server.fetch(messages, 'RFC822').items():
                    msg = email.message_from_bytes(data[b'RFC822'])
                    subject = msg['subject']
                    sent_date = email.utils.parsedate_to_datetime(msg['date'])
                    body = ""
                    attachments = []

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_disposition = part.get("Content-Disposition", "")
                            if "attachment" in content_disposition:
                                # Save attachment
                                filename = part.get_filename()
                                attachment_data = part.get_payload(decode=True)
                                path = os.path.join(settings.MEDIA_ROOT, filename)
                                with open(path, 'wb') as f:
                                    f.write(attachment_data)
                                attachments.append(filename)
                            elif part.get_content_type() == "text/plain":
                                body += part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()

                    if not EmailMessage.objects.filter(subject=subject, sent_date=sent_date).exists():
                        EmailMessage.objects.create(
                            subject=subject,
                            sent_date=sent_date,
                            received_date=sent_date,
                            body=body,
                            attachments=attachments
                        )

                    total_emails_checked += 1
                    progress_percentage = (total_emails_checked / total_emails) * 100

                    # Send progress update through WebSocket
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "email_progress",
                        {
                            "type": "send_progress_update",
                            "progress": progress_percentage,
                        },
                    )
        except Exception as e:
            print(f"Error fetching emails for {credential.email}: {e}")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        messages = EmailMessage.objects.values('id', 'subject', 'sent_date', 'received_date', 'body', 'attachments')
        return JsonResponse({'messages': list(messages)})

    return render(request, 'email_manager/message_list.html', {'messages': EmailMessage.objects.all()})

def email_progress(request):
    total_emails = EmailMessage.objects.count()
    checked_emails = total_emails // 2  # Update this logic to track progress correctly
    progress_percentage = (checked_emails / total_emails) * 100 if total_emails > 0 else 0
    return JsonResponse({'progress': progress_percentage})

def message_list(request):
    fetch_emails_view(request)  
    messages = EmailMessage.objects.all()
    return render(request, 'email_manager/message_list.html', {'messages': messages})
