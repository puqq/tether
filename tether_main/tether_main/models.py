from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Relationship(models.Model):
    FAMILY = 'family'
    FRIEND = 'friend'
    COWORKER = 'coworker'
    OTHER = 'other'
    RELATIONSHIP_CHOICES = [
        (FAMILY, 'Family'),
        (FRIEND, 'Friend'),
        (COWORKER, 'Coworker'),
        (OTHER, 'Other'),
    ]

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    REMINDER_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly')
    ]

    def assign_random_slot(self):
         if self.reminder_frequency == self.WEEKLY:
             self.weekly_day = random.randint(0,6)
         elif self.reminder_frequency == self.MONTHLY:
             self.monthly_day = random.randint(1,28)
         self.save(update_fields=['weekly_day','monthly_day'])

    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationships', db_index=True)
    contact_name       = models.CharField(max_length=255, blank=True, null=True)
    contact_email      = models.EmailField(blank=True, null=True)
    relationship_type  = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, default=FRIEND)
    favorite           = models.BooleanField(default=False)
    reminder_frequency = models.CharField(max_length=50, choices=REMINDER_CHOICES, default=WEEKLY)
    time_of_day        = models.TimeField(default=timezone.datetime.strptime("18:30","%H:%M").time())
    weekly_day         = models.IntegerField(null=True, blank=True)   # 0=Sunday…6=Saturday
    monthly_day        = models.IntegerField(null=True, blank=True)   # 1…28
    last_contacted     = models.DateTimeField(blank=True, null=True)
    notes              = models.TextField(blank=True, null=True)
    paused             = models.BooleanField(default=False, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'contact_email'], name='unique_user_contact_email')
        ]

    def __str__(self):
        return f"{self.contact_name} ({self.relationship_type})"
