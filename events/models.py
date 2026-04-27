from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location_name = models.CharField(max_length=255)
    location_address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    profile_photo = models.URLField()

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
