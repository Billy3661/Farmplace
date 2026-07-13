from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('courses/', views.dashboard_courses, name='courses'),
    path('ebooks/', views.dashboard_ebooks, name='ebooks'),
    path('orders/', views.dashboard_orders, name='orders'),
    path('payments/', views.dashboard_payments, name='payments'),
]
