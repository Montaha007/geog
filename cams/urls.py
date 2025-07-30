from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:location_id>/', views.add_camera, name='add_camera'),
    path('record/<int:camera_id>/', views.record_view, name='record_view'),
    path('alerts/', views.get_fire_alerts, name='get_fire_alerts'),
    path('notification-status/', views.notification_status, name='notification_status'),
    path('test-alert/', views.test_fire_alert, name='test_fire_alert'),
    path('save-alert/', views.save_fire_alert, name='save_fire_alert'),
]
