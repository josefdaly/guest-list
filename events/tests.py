import datetime

from django.test import TestCase
from django.urls import reverse

from events.models import Event, EventPost
from guests.models import Guest


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_event(**kwargs):
    defaults = {
        'name': 'Test Party',
        'date': datetime.date(2026, 6, 1),
        'time': datetime.time(19, 0),
        'location_name': 'The Venue',
        'location_address': '123 Main St',
        'contact_email': 'host@example.com',
        'profile_photo': 'https://example.com/photo.jpg',
        'event_description': 'A great time',
        'music_url': '',
    }
    defaults.update(kwargs)
    return Event.objects.create(**defaults)


_guest_counter = 0

def make_guest(event, **kwargs):
    global _guest_counter
    _guest_counter += 1
    defaults = {
        'first_name': 'Guest',
        'last_name': f'Number{_guest_counter}',
        'email': f'guest{_guest_counter}@example.com',
        'rsvp_status': None,
        'additional_guests': 0,
        'additional_confirmed': 0,
        'profile_photo_url': '',
    }
    defaults.update(kwargs)
    return Guest.objects.create(event=event, **defaults)


# ── Event model ───────────────────────────────────────────────────────────────

class EventModelTests(TestCase):
    def test_str(self):
        event = make_event(name='Summer Bash')
        self.assertEqual(str(event), 'Summer Bash')


# ── EventPost model ───────────────────────────────────────────────────────────

class EventPostModelTests(TestCase):
    def setUp(self):
        self.event = make_event()

    def test_str(self):
        post = EventPost.objects.create(event=self.event, title='Hello World', content='body')
        self.assertEqual(str(post), 'Hello World')

    def test_default_category_is_other(self):
        post = EventPost.objects.create(event=self.event, title='Post', content='body')
        self.assertEqual(post.category, 'Other')

    def test_ordering_newest_first(self):
        post1 = EventPost.objects.create(event=self.event, title='First', content='a')
        post2 = EventPost.objects.create(event=self.event, title='Second', content='b')
        posts = list(self.event.posts.all())
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], post1)

    def test_related_name_posts(self):
        EventPost.objects.create(event=self.event, title='A', content='a')
        EventPost.objects.create(event=self.event, title='B', content='b')
        self.assertEqual(self.event.posts.count(), 2)

    def test_posts_deleted_with_event(self):
        EventPost.objects.create(event=self.event, title='A', content='a')
        self.event.delete()
        self.assertEqual(EventPost.objects.count(), 0)

    def test_category_choices(self):
        valid = ['Life', 'News', 'Parties', 'Music', 'Rants', 'Other']
        for cat in valid:
            post = EventPost.objects.create(event=self.event, title=cat, content='x', category=cat)
            self.assertEqual(post.category, cat)


# ── event_detail view ─────────────────────────────────────────────────────────

class EventDetailViewTests(TestCase):
    def setUp(self):
        self.event = make_event()
        self.url = reverse('events:detail', args=[self.event.pk])

    def test_200_for_valid_event(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_404_for_missing_event(self):
        self.assertEqual(self.client.get(reverse('events:detail', args=[99999])).status_code, 404)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.client.get(self.url), 'events/event_detail.html')

    def test_context_contains_event(self):
        self.assertEqual(self.client.get(self.url).context['event'], self.event)

    def test_event_name_rendered(self):
        self.assertContains(self.client.get(self.url), self.event.name)

    def test_context_confirmed(self):
        make_guest(self.event, rsvp_status=True)
        make_guest(self.event, rsvp_status=True)
        make_guest(self.event, rsvp_status=False)
        self.assertEqual(self.client.get(self.url).context['confirmed'].count(), 2)

    def test_context_declined(self):
        make_guest(self.event, rsvp_status=False)
        make_guest(self.event, rsvp_status=True)
        self.assertEqual(self.client.get(self.url).context['declined'].count(), 1)

    def test_context_pending(self):
        make_guest(self.event, rsvp_status=None)
        make_guest(self.event, rsvp_status=None)
        make_guest(self.event, rsvp_status=True)
        self.assertEqual(self.client.get(self.url).context['pending'].count(), 2)

    def test_total_attending_includes_additional_confirmed(self):
        make_guest(self.event, rsvp_status=True, additional_confirmed=2)
        make_guest(self.event, rsvp_status=True, additional_confirmed=0)
        make_guest(self.event, rsvp_status=False, additional_confirmed=3)
        # (1+2) + (1+0) = 4; declined guest not counted
        self.assertEqual(self.client.get(self.url).context['total_attending'], 4)

    def test_total_attending_zero_when_no_confirmed(self):
        make_guest(self.event, rsvp_status=False)
        make_guest(self.event, rsvp_status=None)
        self.assertEqual(self.client.get(self.url).context['total_attending'], 0)

    def test_total_attending_zero_with_no_guests(self):
        self.assertEqual(self.client.get(self.url).context['total_attending'], 0)

    def test_context_posts(self):
        EventPost.objects.create(event=self.event, title='Post 1', content='body')
        EventPost.objects.create(event=self.event, title='Post 2', content='body')
        self.assertEqual(self.client.get(self.url).context['posts'].count(), 2)

    def test_posts_from_other_event_excluded(self):
        other = make_event(name='Other', contact_email='other@example.com')
        EventPost.objects.create(event=other, title='Theirs', content='x')
        EventPost.objects.create(event=self.event, title='Ours', content='x')
        self.assertEqual(self.client.get(self.url).context['posts'].count(), 1)

    def test_guests_from_other_event_excluded(self):
        other = make_event(name='Other', contact_email='other@example.com')
        make_guest(self.event, rsvp_status=True)
        make_guest(other, rsvp_status=True)
        self.assertEqual(self.client.get(self.url).context['guests'].count(), 1)

    def test_no_guests_returns_empty_querysets(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['guests'].count(), 0)
        self.assertEqual(response.context['confirmed'].count(), 0)
        self.assertEqual(response.context['declined'].count(), 0)
        self.assertEqual(response.context['pending'].count(), 0)
