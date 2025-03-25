from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(
        get_user_model(),
        related_name='events_attending',
        blank=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['name']),
        ]

    @property
    def is_past(self):
        return self.date < timezone.now()


    def add_attendee(self, user):
        if self.is_past:
            raise ValidationError("Cannot attend past events")

        if user in self.attendees.all():
            raise ValidationError("User is already attending this event")

        self.attendees.add(user)

    def remove_attendee(self, user):
        if user not in self.attendees.all():
            raise ValidationError("User is not attending this event")

        self.attendees.remove(user)
