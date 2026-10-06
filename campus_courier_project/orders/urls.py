from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('orders/new/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/cancel/', views.order_cancel_view, name='order_cancel'),
    path('orders/<int:pk>/rate/', views.rate_order_view, name='order_rate'),
    path('api/order/<int:pk>/status/', views.order_status_json, name='order_status_json'),
    path('api/campus-bounds/', views.campus_bounds_view, name='campus_bounds'),
    path('api/landmarks/', views.landmarks_json_view, name='landmarks_json'),
    path('api/estimate-distance/', views.distance_estimate_view, name='distance_estimate'),
    path('api/reverse-geocode/', views.reverse_geocode_view, name='reverse_geocode'),
    path('api/hotspots/', views.hotspots_view, name='hotspots'),
    path('api/hotspots/json/', views.hotspots_view, name='hotspots_json'),
    path('api/order/<int:pk>/messages/', views.order_messages_list, name='order_messages_list'),
    path('api/order/<int:pk>/messages/create/', views.order_messages_create, name='order_messages_create'),
]
