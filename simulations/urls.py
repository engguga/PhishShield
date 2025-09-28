from django.urls import path
from . import views

app_name = 'simulations'

urlpatterns = [
    path('track/<uuid:unique_id>/', views.track_click, name='track_click'),
]
