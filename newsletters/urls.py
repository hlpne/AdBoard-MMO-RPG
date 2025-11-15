"""
URLs for newsletters app.
"""
from django.urls import path
from . import views

app_name = 'newsletters'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('templates/', views.template_list, name='template_list'),
    path('send/<int:template_id>/', views.send_newsletter_view, name='send'),
]

