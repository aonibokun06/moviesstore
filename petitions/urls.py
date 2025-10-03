from django.urls import path
from . import views

urlpatterns = [
    path('', views.petition_list, name='petitions.list'),
    path('create/', views.create_petition, name='petitions.create'),
    path('<int:petition_id>/vote/', views.vote_petition, name='petitions.vote'),
    path('<int:petition_id>/', views.petition_detail, name='petitions.detail'),
]
