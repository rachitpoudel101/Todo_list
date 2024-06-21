from django.urls import path
from . import views

urlpatterns = [
    path('todos', views.TodoListCreate.as_view()),
    path('todos/completed', views.TodoCompletedList.as_view()),
]
