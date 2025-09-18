from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<str:cart_id>/', views.view_cart, name='cart.view_cart'),
    path('<int:id>/add/<str:cart_id>/', views.add, name='cart.add'),
    path('<str:cart_id>/clear/', views.clear, name='cart.clear'),
    path('<str:cart_id>/purchase/', views.purchase, name='cart.purchase'),
]