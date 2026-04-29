from django import forms

from events.models import Event, EventPost


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'event_description': forms.Textarea(attrs={'rows': 4}),
            'music_url': forms.Textarea(attrs={'rows': 3}),
            'marquee_banner_text': forms.Textarea(attrs={'rows': 2}),
        }
        help_texts = {
            'music_url': 'Paste an iframe embed code (e.g. from YouTube or Spotify). Leave blank for the animated placeholder.',
            'profile_photo': 'URL to the event profile image.',
            'background_url': 'URL to an image used as the page background. Leave blank for the default starfield.',
            'marquee_banner_text': 'Scrolling text shown in the profile header. Leave blank to hide.',
        }


class EventPostForm(forms.ModelForm):
    class Meta:
        model = EventPost
        fields = ['title', 'category', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }
        help_texts = {
            'content': 'HTML is supported and rendered directly on the event page.',
        }
