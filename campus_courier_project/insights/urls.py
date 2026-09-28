from django.urls import path
from . import views

urlpatterns = [
    path('', views.insights_dashboard, name='insights_dashboard'),
    path('orders/', views.insights_orders, name='insights_orders'),
    path('users/', views.insights_users, name='insights_users'),
    path('audit/', views.insights_audit, name='insights_audit'),
]
