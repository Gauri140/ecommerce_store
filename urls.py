# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect_view, name='home'),
    path('products/', views.product_list, name='product_list'),
path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('order-history/', views.order_history, name='order_history'),
    path('search/', views.search_products, name='search_products'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),


]
