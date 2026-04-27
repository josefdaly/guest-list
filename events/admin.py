from django.contrib import admin

from events.models import Event, EventPost


@admin.register(EventPost)
class EventPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'category', 'created_at')
    list_filter = ('event', 'category')


admin.site.register(Event)
