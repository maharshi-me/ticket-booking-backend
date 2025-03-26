from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event, EventAttendance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name']

class MyAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendance
        fields = ['fee_paid', 'registered_at']
        read_only_fields = fields

class EventSerializer(serializers.ModelSerializer):
    attendees = UserSerializer(many=True, read_only=True)
    is_attending = serializers.SerializerMethodField()
    my_attendance = serializers.SerializerMethodField()
    discounted_fee = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'fee', 'discounted_fee',
                 'attendees', 'is_attending', 'my_attendance']
        read_only_fields = fields

    def get_is_attending(self, obj):
        user = self.context['request'].user
        return obj.eventattendance_set.filter(user=user).exists()

    def get_my_attendance(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        try:
            attendance = obj.eventattendance_set.get(user=user)
            return MyAttendanceSerializer(attendance).data
        except EventAttendance.DoesNotExist:
            return None

    def get_discounted_fee(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return obj.fee
        return str(obj.get_fee_for_user(user))


class SimpleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name']

class EventAttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = SimpleEventSerializer(read_only=True)

    class Meta:
        model = EventAttendance
        fields = ['fee_paid', 'registered_at', 'event', 'user']
        read_only_fields = ['fee_paid', 'registered_at', 'event', 'user']