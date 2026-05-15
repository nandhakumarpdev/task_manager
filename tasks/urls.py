from django.urls import path
from .views import AllTaskView, TaskView, UserRegistration, UserLogin

urlpatterns = [
    #path('', views.hello),
    # Account
    path("account/user-register/", UserRegistration.as_view(), name="user-register"),
    path("account/login/", UserLogin.as_view(), name="user-login"),

    # Worklist
    path("get-tasks/<int:user_id>",AllTaskView.as_view(), name="get-all-tasks"),
    path("get-task/<int:id>", TaskView.as_view(), name="get-task"),
    path("update-task/<int:id>", TaskView.as_view(), name="update-task"),
    path("add-task/", AllTaskView.as_view(), name="add-task"),
    path("delete-task/<int:id>", TaskView.as_view(), name="delete-task"),
]