# tether_main/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Relationship

@shared_task
def send_reminder_email(rel_id):
    rel = Relationship.objects.get(pk=rel_id)
    user_email = rel.user.email
    if not user_email:
        return

    subject = f"Time to connect with {rel.contact_name}"
    message = (
        f"Hi {rel.user.username},\n\n"
        f"Remember to reach out to {rel.contact_name} today!\n\n"
        "— Your friends at Tether"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
