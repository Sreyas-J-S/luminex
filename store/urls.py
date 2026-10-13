"""Store URL patterns."""
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Catalog
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),

    # Cart & Bag
    path('bag/', views.cart_detail, name='cart_detail'),
    path('bag/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('bag/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('bag/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
]
