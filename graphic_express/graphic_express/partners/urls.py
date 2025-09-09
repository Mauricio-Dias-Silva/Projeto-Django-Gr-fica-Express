from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('register/', views.partner_register, name='partner_register'),
    path('dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('orders/', views.partner_orders, name='partner_orders'),
]