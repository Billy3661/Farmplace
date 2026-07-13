from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<str:purpose>/<int:reference_id>/', views.initiate_payment, name='initiate_payment'),
    path('<int:pk>/', views.payment_detail, name='payment_detail'),
    path('<int:pk>/status/', views.payment_status, name='payment_status'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
]
