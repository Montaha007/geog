
from django.urls import path
from . import views
urlspatterns = [
    path('add/<int:location_id>/', views.add_camera, name='add_camera'),
]       