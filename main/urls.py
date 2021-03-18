from django.urls import path
from .views import ListTodo,  api_root

urlpatterns = [
path('', api_root),
]
