from django.urls import path 
from . import views

urlpatterns = [
    path('todo/', views.TodoListView),
    path('todo/create/', views.TodoCreateView),
    path('todo/detail/<str:id>/', views.TodoTaskDetailView),

    path('news/', views.newsListView),
    path('news/<str:id>', views.newsDetailView),
]
