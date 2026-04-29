from django.contrib import admin

from events.models import Event, EventComment, EventPost


@admin.register(EventPost)
class EventPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'category', 'created_at')
    list_filter = ('event', 'category')


@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'event', 'created_at', 'approved')
    list_editable = ('approved',)
    list_filter = ('approved', 'event')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'owner')
    list_select_related = ('owner',)
    raw_id_fields = ('owner',)
