from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Relationship

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = [
            'id', 'contact_name', 'contact_email', 'relationship_type',
            'favorite', 'reminder_frequency', 'last_contacted',
            'notes', 'paused'
        ]
        read_only_fields = ('user',)
