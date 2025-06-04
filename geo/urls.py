# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('geo/', views.location, name='location'),
    #path('geo/<int:location_id>/', views.location_detail, name='location_detail'),
    #path('geo/create/', views.create_location, name='create_location'),
]
