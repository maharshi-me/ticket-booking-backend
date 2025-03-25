from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer, AttendanceActionSerializer

class EventListView(generics.ListAPIView):
    """List all events."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

class EventDetailView(generics.RetrieveAPIView):
    """Retrieve a specific event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class AttendEventView(generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = AttendanceActionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(
            data={},
            context={'request': request, 'event': event, 'action': 'attend'}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            getattr(serializer, 'attend')(),
            status=status.HTTP_200_OK
        )

class UnattendEventView(generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = AttendanceActionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(
            data={},
            context={'request': request, 'event': event, 'action': 'unattend'}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            getattr(serializer, 'unattend')(),
            status=status.HTTP_200_OK
        )