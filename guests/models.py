from django.db import models

# Create your models here.
class Guest(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    rsvp_status = models.BooleanField(null=True, blank=True)
    additional_guests = models.IntegerField(default=0)
    additional_confirmed = models.IntegerField(default=0)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='guests')

    profile_photo_url = models.URLField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
