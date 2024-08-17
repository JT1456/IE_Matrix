# tasks/urls.py
from django.urls import path
from .views import matrix

urlpatterns = [
    path('', matrix, name='task_matrix'),  # This will be your home page
]