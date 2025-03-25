from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name']

class EventSerializer(serializers.ModelSerializer):
    attendees = UserSerializer(many=True, read_only=True)
    is_attending = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_is_attending(self, obj):
        user = self.context['request'].user
        return user in obj.attendees.all() if user.is_authenticated else False
