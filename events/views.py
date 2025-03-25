from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)

class AttendEventView(generics.GenericAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user in event.attendees.all():
            return Response({
                "message": "You are already attending this event"
            }, status=status.HTTP_400_BAD_REQUEST)

        event.attendees.add(request.user)
        return Response({
            "message": "Successfully registered for the event"
        }, status=status.HTTP_200_OK)

class UnattendEventView(generics.GenericAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user not in event.attendees.all():
            return Response({
                "message": "You are not attending this event"
            }, status=status.HTTP_400_BAD_REQUEST)

        event.attendees.remove(request.user)
        return Response({
            "message": "Successfully unregistered from the event"
        }, status=status.HTTP_200_OK)