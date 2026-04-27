from django.shortcuts import get_object_or_404, render

from .models import Event, EventComment, EventPost


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    guests = event.guests.all()
    confirmed = guests.filter(rsvp_status=True)
    declined = guests.filter(rsvp_status=False)
    pending = guests.filter(rsvp_status__isnull=True)
    total_attending = sum(g.additional_confirmed + 1 for g in confirmed)
    posts = event.posts.all()
    comments = EventComment.objects.filter(event=event, approved=True)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'guests': guests,
        'confirmed': confirmed,
        'declined': declined,
        'pending': pending,
        'total_attending': total_attending,
        'posts': posts,
        'comments': comments,
    })
