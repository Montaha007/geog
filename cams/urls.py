from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:location_id>/', views.add_camera, name='add_camera'),
    path('record/<int:camera_id>/', views.record_view, name='record_view'),
]