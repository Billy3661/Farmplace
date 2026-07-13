from django.urls import path
from . import views

app_name = 'chicks'

urlpatterns = [
    path('', views.chicks_catalog, name='catalog'),
    path('type/<str:breed>/', views.chick_type_detail, name='type_detail'),
    path('order/<int:batch_id>/', views.order_chicks, name='order_chicks'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
