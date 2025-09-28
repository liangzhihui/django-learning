from django.urls import path, include
from . import views

urlpatterns = [
    path("fbv/list/", views.course_list, name='fbv-list'),
    path('fbv/detail/<int:pk>/', views.course_detail, name='fbv-detail'),
]