from django.urls import path
from . import views

app_name = 'ebooks'

urlpatterns = [
    path('', views.ebook_list, name='ebook_list'),
    path('<slug:slug>/', views.ebook_detail, name='ebook_detail'),
    path('<slug:slug>/purchase/', views.purchase_ebook, name='purchase_ebook'),
    path('<slug:slug>/download/', views.download_ebook, name='ebook_download'),
]
