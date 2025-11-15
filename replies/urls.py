"""
URLs for replies app.
"""
from django.urls import path
from . import views

app_name = 'replies'

urlpatterns = [
    path('create/', views.reply_create, name='create'),
    path('my/', views.my_replies, name='my_replies'),
    path('<int:pk>/accept/', views.reply_accept, name='accept'),
    path('<int:pk>/delete/', views.reply_delete, name='delete'),
]

