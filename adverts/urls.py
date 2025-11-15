"""
URLs for adverts app.
"""
from django.urls import path
from . import views

app_name = 'adverts'

urlpatterns = [
    path('', views.advert_list, name='list'),
    path('create/', views.advert_create, name='create'),
    path('<int:pk>/', views.advert_detail, name='detail'),
    path('<int:pk>/edit/', views.advert_edit, name='edit'),
    path('<int:pk>/delete/', views.advert_delete, name='delete'),
]

