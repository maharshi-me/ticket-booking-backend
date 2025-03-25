from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event
from django.core.exceptions import ValidationError

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

class EventAttendanceSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)

    def attend(self):
        event = self.context['event']
        user = self.context['request'].user
        try:
            event.add_attendee(user)
            return {"message": "Successfully registered for the event"}
        except ValidationError as e:
            raise serializers.ValidationError({
                "error": str(e.message)
            })

    def unattend(self):
        event = self.context['event']
        user = self.context['request'].user
        try:
            event.remove_attendee(user)
            return {"message": "Successfully unregistered from the event"}
        except ValidationError as e:
            raise serializers.ValidationError({
                "error": str(e.message)
            })
