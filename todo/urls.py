from django.urls import path
from . import views
from .views import CreateBucket, CreateTodo

urlpatterns = [
    path('create-bucket', CreateBucket.as_view(), name='createbucket'),
    path('create-todo', CreateTodo.as_view(), name='createtodo'),
]
