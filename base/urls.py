from django.urls import path
from . import views

urlpatterns = [
    # Page Routes
    path('profile/', views.profile, name='profile'),
    path('order-history', views.order_history, name='order_history'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('vouchers/', views.vouchers_view, name='vouchers'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('sarwana-bhawan/', views.SarwanaBhawan, name='SarwanaBhawan'),
    path('mughals-kitchen/', views.MughalsKitchen, name='MughalsKitchen'),
    path('taj-palace/', views.TajPalace, name='TajPalace'),
    path('punjab-grill/', views.PunjabGrill, name='PunjabGrill'),
    path('dosa-plaza/', views.DosaPlaza, name='DosaPlaza'),
    path('biryani-house/', views.BiryaniHouse, name='BiryaniHouse'),
    path('payment/', views.payment, name='payment'),
    
    # API Routes
    path('api/signup/', views.SignupAPI.as_view(), name='signup_api'),
    path('api/login/', views.LoginAPI.as_view(), name='login_api'),
]
