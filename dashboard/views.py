from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from events.models import Event, EventComment, EventPost
from .forms import EventForm, EventPostForm

_LOGIN_URL = '/dashboard/login/'


def _get_event(user):
    return Event.objects.filter(owner=user).first()


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard:home')
    return render(request, 'dashboard/login.html', {'form': form})


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard:login')


@login_required(login_url=_LOGIN_URL)
def home(request):
    event = _get_event(request.user)
    ctx = {'event': event}
    if event:
        confirmed = event.guests.filter(rsvp_status=True)
        ctx.update({
            'confirmed_count': confirmed.count(),
            'declined_count': event.guests.filter(rsvp_status=False).count(),
            'pending_count': event.guests.filter(rsvp_status__isnull=True).count(),
            'total_attending': sum(g.additional_confirmed + 1 for g in confirmed),
            'pending_comments': event.comments.filter(approved=False).count(),
            'post_count': event.posts.count(),
        })
    return render(request, 'dashboard/home.html', ctx)


@login_required(login_url=_LOGIN_URL)
def event_edit(request):
    event = _get_event(request.user)
    form = EventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        ev = form.save(commit=False)
        ev.owner = request.user
        ev.save()
        return redirect('dashboard:home')
    return render(request, 'dashboard/event_form.html', {'form': form, 'event': event})


@login_required(login_url=_LOGIN_URL)
def posts(request):
    event = _get_event(request.user)
    if not event:
        return redirect('dashboard:event_edit')
    return render(request, 'dashboard/posts.html', {'event': event, 'posts': event.posts.all()})


@login_required(login_url=_LOGIN_URL)
def post_create(request):
    event = _get_event(request.user)
    if not event:
        return redirect('dashboard:event_edit')
    form = EventPostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.event = event
        post.save()
        return redirect('dashboard:posts')
    return render(request, 'dashboard/post_form.html', {'form': form, 'action': 'New Post', 'event': event})


@login_required(login_url=_LOGIN_URL)
def post_edit(request, pk):
    event = _get_event(request.user)
    post = get_object_or_404(EventPost, pk=pk, event=event)
    form = EventPostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:posts')
    return render(request, 'dashboard/post_form.html', {'form': form, 'action': 'Edit Post', 'event': event})


@login_required(login_url=_LOGIN_URL)
@require_POST
def post_delete(request, pk):
    event = _get_event(request.user)
    post = get_object_or_404(EventPost, pk=pk, event=event)
    post.delete()
    return redirect('dashboard:posts')


@login_required(login_url=_LOGIN_URL)
def comments(request):
    event = _get_event(request.user)
    if not event:
        return redirect('dashboard:event_edit')
    comment_list = event.comments.order_by('approved', '-created_at')
    return render(request, 'dashboard/comments.html', {'event': event, 'comments': comment_list})


@login_required(login_url=_LOGIN_URL)
@require_POST
def comment_approve(request, pk):
    event = _get_event(request.user)
    comment = get_object_or_404(EventComment, pk=pk, event=event)
    comment.approved = True
    comment.save()
    return redirect('dashboard:comments')


@login_required(login_url=_LOGIN_URL)
@require_POST
def comment_delete(request, pk):
    event = _get_event(request.user)
    comment = get_object_or_404(EventComment, pk=pk, event=event)
    comment.delete()
    return redirect('dashboard:comments')


@login_required(login_url=_LOGIN_URL)
def guests(request):
    event = _get_event(request.user)
    if not event:
        return redirect('dashboard:event_edit')
    guest_list = event.guests.order_by('last_name', 'first_name')
    return render(request, 'dashboard/guests.html', {'event': event, 'guests': guest_list})
