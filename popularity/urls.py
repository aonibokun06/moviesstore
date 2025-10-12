from django.urls import path
from . import views

urlpatterns = [
    path('', views.popularity_map, name='map'),
    path('region/<int:region_id>/', views.region_details, name='region_details'),
    path('update-data/', views.update_popularity_data, name='update_data'),
]
