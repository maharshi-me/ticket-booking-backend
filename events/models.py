from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

User = get_user_model()
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(
        User,
        through='EventAttendance',
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
        event_date = timezone.localtime(self.date)
        now = timezone.localtime(timezone.now())
        return event_date < now

    def get_fee_for_user(self, user):
        if user.gender == 'F':
            return round(self.fee * Decimal('0.95'), 2)
        return self.fee

    def add_attendee(self, user):
        if self.is_past:
            raise ValidationError("Cannot attend past events")

        if self.eventattendance_set.filter(user=user).exists():
            raise ValidationError("User is already attending this event")

        attendance = EventAttendance.objects.create(
            event=self,
            user=user,
            fee_paid=self.get_fee_for_user(user)
        )

        return attendance

    def remove_attendee(self, user):
        attendance = self.eventattendance_set.filter(user=user).first()
        if self.is_past:
            raise ValidationError("Cannot unattend from past events")
        if not attendance:
            raise ValidationError("User is not attending this event")
        attendance.delete()

class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fee_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.email} - {self.event.name} (Paid: {self.fee_paid})"
