from django.urls import path
from .views import ListTodo, DetailTodo, api_root

urlpatterns = [
path('<int:pk>', DetailTodo.as_view()),
path('', api_root),
]
