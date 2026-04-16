from django.urls import path
from .views import TaskView 

urlpatterns = [
    #path('', views.hello),
    path('get-tasks/', TaskView.as_view(), name="get-all-tasks"),
    path('add-task/', TaskView.as_view(), name="add-task"),
]