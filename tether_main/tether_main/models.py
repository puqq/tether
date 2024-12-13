from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Relationship Model
from django.contrib.auth.models import User
from django.db import models

# Enum for different types of relationships
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationships')
    contact_name = models.CharField(max_length=255, null=True, blank=True)  # Make name nullable
    contact_email = models.EmailField(null=True, blank=True)  # Make email nullable
    relationship_type = models.CharField(
        max_length=50, choices=RELATIONSHIP_CHOICES, default=FRIEND
    )
    favorite = models.BooleanField(default=False)  # Whether this is a favorite contact
    reminder_frequency = models.CharField(
        max_length=50,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        default='weekly'
    )
    last_contacted = models.DateTimeField(null=True, blank=True)  # When was the last time the user contacted this person
    notes = models.TextField(blank=True, null=True)  # Additional notes about the contact
    paused = models.BooleanField(default=False)  # Pause reminders for this contact

    def __str__(self):
        return f"{self.contact_name} ({self.relationship_type})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'contact_email'], name='unique_user_contact_email')
        ]

# Reminder Model: Linked to the relationship model
class Reminder(models.Model):
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, related_name='reminders', null=True, blank=True)
    reminder_type = models.CharField(
        max_length=6,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    )
    reminder_time = models.DateTimeField(default=timezone.now)  # Set default time to now
    created_at = models.DateTimeField(auto_now_add=True)  # When the reminder was created

    def __str__(self):
        return f"Reminder for {self.relationship.contact_name} at {self.reminder_time}"

# Notification Model: Stores notifications related to the user
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()  # Notification message
    status = models.CharField(
        max_length=7,
        choices=[('pending', 'Pending'), ('sent', 'Sent')]
    )
    created_at = models.DateTimeField(auto_now_add=True)  # When the notification was created
    is_active = models.BooleanField(default=True)  # Is the notification still active?

    def __str__(self):
        return f"Notification for {self.user.username} - {self.status}"
