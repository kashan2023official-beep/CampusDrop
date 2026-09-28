from django.urls import path
from . import views

urlpatterns = [
    path('available/', views.available_orders_view, name='courier_available'),
    path('available/json/', views.available_orders_json, name='courier_available_json'),
    path('accept/<int:pk>/', views.accept_order_view, name='courier_accept'),
    path('pickup/<int:pk>/', views.pickup_order_view, name='courier_pickup'),
    path('deliver/<int:pk>/', views.deliver_order_view, name='courier_deliver'),
    path('jobs/', views.my_jobs_view, name='courier_jobs'),
]
