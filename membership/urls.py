from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('', views.membership_plans, name='plans'),
    path('subscribe/<slug:plan_slug>/', views.subscribe, name='subscribe'),
    path('status/', views.membership_status, name='status'),
]
