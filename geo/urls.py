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
    
]
