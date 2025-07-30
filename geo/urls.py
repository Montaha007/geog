# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.location, name='location'),
    path('geo/save/', views.save_geojson, name='save_geojson'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),  
    path('history/', views.history_view, name='history'),
    path('download/<int:pk>/', views.download_location, name='download'),
    path('delete/<int:pk>/', views.delete_location, name='delete'),
    
    # Fire Detection Alert Management URLs
    path('api/fire-alerts/webhook/', views.fire_alert_webhook, name='fire_alert_webhook'),
    path('api/fire-alerts/', views.get_fire_alerts, name='get_fire_alerts'),
    path('api/fire-alerts/<int:alert_id>/resolve/', views.resolve_fire_alert, name='resolve_fire_alert'),
    path('api/fire-alerts/<int:alert_id>/delete/', views.delete_fire_alert, name='delete_fire_alert'),
    path('api/fire-alerts/bulk-resolve/', views.bulk_resolve_alerts, name='bulk_resolve_alerts'),
    path('api/fire-alerts/export/', views.export_fire_alerts, name='export_fire_alerts'),
    path('fire-alerts/dashboard/', views.fire_alerts_dashboard, name='fire_alerts_dashboard'),
    path('demo/alerts/', views.alert_demo_view, name='alert_demo'),
]
