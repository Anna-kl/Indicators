from django.urls import path
from .views import ListTodo,  api_root, DetailTodo, get_staff, api_main, api_test, api_root1, api_root2

urlpatterns = [
path('<int:pk>', DetailTodo.as_view()),
path('', api_root),
path('staff', get_staff),
    path('main', api_main),
path('test', api_test),
path('test1', api_root1),
path('test2', api_root2)
]
