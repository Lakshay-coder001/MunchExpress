from django.urls import path
from . import views

app_name = 'munchmart'

urlpatterns = [
    path('', views.index, name='index'),  # Use views.index here
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
]

