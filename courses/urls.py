from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('<slug:slug>/learn/', views.course_learn, name='course_learn'),
    path('<slug:slug>/complete/<int:lesson_id>/', views.complete_lesson, name='complete_lesson'),
]
