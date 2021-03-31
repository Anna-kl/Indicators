from django.urls import path
from .views import ListTodo,  api_root, DetailTodo, get_staff, api_main

urlpatterns = [
path('<int:pk>', DetailTodo.as_view()),
path('', api_root),
path('staff', get_staff),
    path('main', api_main)
]
