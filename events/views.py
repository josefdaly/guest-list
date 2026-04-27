from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .forms import EventCommentForm
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
    comment_form = EventCommentForm()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'guests': guests,
        'confirmed': confirmed,
        'declined': declined,
        'pending': pending,
        'total_attending': total_attending,
        'posts': posts,
        'comments': comments,
        'comment_form': comment_form,
    })


@require_POST
def add_comment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = EventCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.event = event
        comment.approved = False
        comment.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
