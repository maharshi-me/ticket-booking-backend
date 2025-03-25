from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from events.models import Event, EventAttendance
from decimal import Decimal
import random
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        EventAttendance.objects.all().delete()
        Event.objects.all().delete()
        get_user_model().objects.all().delete()

        # Create sample users
        self.stdout.write('Creating sample users...')
        users = []
        for i in range(5):
            user = get_user_model().objects.create_user(
                email=f'user{i+1}@example.com',
                password='testpass123',
                name=f'Test User {i+1}',
                gender='M' if i % 2 == 0 else 'F'
            )
            users.append(user)

        # Sample events data with timezone-aware future dates
        events_data = [
            {
                'name': 'New Year Concert 2026',
                'date': timezone.make_aware(datetime(2026, 1, 1, 20, 0)),
                'fee': Decimal('99.99')
            },
            {
                'name': 'Summer Tech Conference',
                'date': timezone.make_aware(datetime(2025, 7, 15, 9, 0)),
                'fee': Decimal('149.99')
            },
            {
                'name': 'Christmas Festival 2025',
                'date': timezone.make_aware(datetime(2025, 12, 25, 18, 0)),
                'fee': Decimal('75.00')
            },
            {
                'name': 'Spring Art Exhibition',
                'date': timezone.make_aware(datetime(2026, 5, 1, 10, 0)),
                'fee': Decimal('25.00')
            },
            {
                'name': 'Winter Sports Tournament',
                'date': timezone.make_aware(datetime(2026, 12, 1, 14, 0)),
                'fee': Decimal('50.00')
            }
        ]

        # Create sample events
        self.stdout.write('Creating sample events...')
        events = []
        for event_data in events_data:
            event = Event.objects.create(
                name=event_data['name'],
                description=f"Join us for the amazing {event_data['name']}! This will be an unforgettable experience.",
                date=event_data['date'],
                fee=event_data['fee']
            )
            events.append(event)

        # Add random attendees with partial payments
        self.stdout.write('Adding attendees...')
        for event in events:
            num_attendees = random.randint(2, 4)
            attendees = random.sample(users, num_attendees)
            for user in attendees:
                event.add_attendee(user)

        self.stdout.write(self.style.SUCCESS(f'''
Successfully seeded database with:
- {len(users)} users
- {len(events)} events
- {EventAttendance.objects.count()} attendances
        '''))