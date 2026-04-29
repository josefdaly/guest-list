from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    path('', views.home, name='home'),
    path('event/', views.event_edit, name='event_edit'),
    path('posts/', views.posts, name='posts'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comments/', views.comments, name='comments'),
    path('comments/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('guests/', views.guests, name='guests'),
]
