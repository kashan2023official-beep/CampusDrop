from django.urls import path
from . import views

urlpatterns = [
    path('api/predict-fare/', views.predict_fare_view, name='predict_fare'),
]
