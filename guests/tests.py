import datetime

from django.test import TestCase

from events.models import Event
from guests.models import Guest


# ── Helper ────────────────────────────────────────────────────────────────────

def make_event():
    return Event.objects.create(
        name='Party',
        date=datetime.date(2026, 6, 1),
        time=datetime.time(19, 0),
        location_name='Venue',
        location_address='123 Main St',
        contact_email='host@example.com',
        profile_photo='https://example.com/photo.jpg',
    )


# ── Guest model ───────────────────────────────────────────────────────────────

class GuestModelTests(TestCase):
    def setUp(self):
        self.event = make_event()

    def test_str(self):
        guest = Guest.objects.create(
            first_name='John', last_name='Smith',
            email='john@example.com', event=self.event,
            profile_photo_url='',
        )
        self.assertEqual(str(guest), 'John Smith')

    def test_default_additional_guests_zero(self):
        guest = Guest.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', event=self.event,
            profile_photo_url='',
        )
        self.assertEqual(guest.additional_guests, 0)

    def test_default_additional_confirmed_zero(self):
        guest = Guest.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', event=self.event,
            profile_photo_url='',
        )
        self.assertEqual(guest.additional_confirmed, 0)

    def test_rsvp_status_defaults_to_none(self):
        guest = Guest.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', event=self.event,
            profile_photo_url='',
        )
        self.assertIsNone(guest.rsvp_status)

    def test_rsvp_status_can_be_true(self):
        guest = Guest.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', event=self.event,
            rsvp_status=True, profile_photo_url='',
        )
        self.assertTrue(guest.rsvp_status)

    def test_rsvp_status_can_be_false(self):
        guest = Guest.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', event=self.event,
            rsvp_status=False, profile_photo_url='',
        )
        self.assertFalse(guest.rsvp_status)

    def test_guest_deleted_with_event(self):
        Guest.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', event=self.event,
            profile_photo_url='',
        )
        self.event.delete()
        self.assertEqual(Guest.objects.count(), 0)

    def test_phone_number_optional(self):
        guest = Guest.objects.create(
            first_name='Jane', last_name='Doe',
            email='jane@example.com', event=self.event,
            profile_photo_url='',
        )
        self.assertIsNone(guest.phone_number)
