from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('<int:event_id>/', views.event_detail, name='detail'),
    path('<int:event_id>/comment/', views.add_comment, name='add_comment'),
]
