from django.urls import path
from . import views

app_name = 'consultancy'

urlpatterns = [
    path('', views.consultancy_list, name='list'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('<int:pk>/book/', views.book_consultation, name='book'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
]
