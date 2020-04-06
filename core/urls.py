from django.contrib import admin
from django.urls import path, include
import core.views as core_views

app_name = 'core'

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('',core_views.HomeView.as_view(),name='item-list'),
    path('checkout/',core_views.CheckoutView.as_view(),name='item-checkout'),
    path('product/<str:pk>',core_views.ItemDetailView.as_view(),name='product'),
    path('add_to_cart/<str:pk>',core_views.add_to_cart,name = 'add-to-cart'),
    path('remove_from_cart/<str:pk>',core_views.remove_from_cart,name = 'remove-from-cart'),
    path('order_summary/',core_views.OrderSummaryView.as_view(),name='order-summary'),
    path('remove_single_item_from_cart/<str:pk>',core_views.remove_single_item_from_cart,name = 'remove-single-item-from-cart'),

]
