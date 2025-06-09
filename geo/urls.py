# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.location, name='location'),
    path('geo/save/', views.save_geojson, name='save_geojson'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),    
    #path('geo/<int:location_id>/', views.location_detail, name='location_detail'),
]
