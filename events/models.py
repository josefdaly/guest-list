from django.db import models


class Event(models.Model):
    BACKGROUND_TILED = 'tiled'
    BACKGROUND_STRETCHED = 'stretched'
    BACKGROUND_DISPLAY_CHOICES = (
        (BACKGROUND_TILED, 'Tiled'),
        (BACKGROUND_STRETCHED, 'Stretched')
    )

    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    event_description = models.TextField(blank=True)
    location_name = models.CharField(max_length=255)
    location_address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    profile_photo = models.URLField()
    music_url = models.TextField(blank=True)
    background_url = models.URLField(blank=True)
    background_display_choice = models.CharField(max_length=255, default=BACKGROUND_TILED, choices=BACKGROUND_DISPLAY_CHOICES)
    marquee_banner_text = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EventPost(models.Model):
    CATEGORY_CHOICES = [
        ('Life', 'Life'),
        ('News', 'News'),
        ('Parties', 'Parties'),
        ('Music', 'Music'),
        ('Rants', 'Rants'),
        ('Other', 'Other'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EventComment(models.Model):
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=255)
    post = models.TextField()
    avatar_url = models.URLField(blank=True)
    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

