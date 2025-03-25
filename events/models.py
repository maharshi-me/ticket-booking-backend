from django.db import models
from django.contrib.auth import get_user_model

class Event(models.Model):
    """Model representing an event."""

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

