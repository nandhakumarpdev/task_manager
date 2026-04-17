from django.urls import path
from .views import AllTaskView, TaskView

urlpatterns = [
    #path('', views.hello),
    path("get-tasks/",AllTaskView.as_view(), name="get-all-tasks"),
    path("add-task/", AllTaskView.as_view(), name="add-task"),
    path("delete-task/<int:id>", TaskView.as_view(), name="delete-task"),
]