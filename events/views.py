from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer, EventAttendanceSerializer
from django.core.exceptions import ValidationError

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class AttendEventView(generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventAttendanceSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event = self.get_object()

        try:
            my_attendance = event.add_attendee(request.user)
        except ValidationError as e:
            return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "message": "Successfully registered for the event",
                "my_attendance": self.get_serializer_class()(my_attendance).data
            },
            status=status.HTTP_200_OK
        )

class UnattendEventView(generics.GenericAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EventAttendanceSerializer

    def post(self, request, *args, **kwargs):
        event = self.get_object()

        try:
            event.remove_attendee(request.user)
        except ValidationError as e:
            return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Successfully unregistered from the event"},
            status=status.HTTP_200_OK
        )