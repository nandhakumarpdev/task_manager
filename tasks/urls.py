from django.urls import path
from .views import AllTaskView, TaskView, UserRegistration, UserLogin, Dashboard

urlpatterns = [
    #path('', views.hello),
    # Account
    path("account/user-register/", UserRegistration.as_view(), name="user-register"),
    path("account/login/", UserLogin.as_view(), name="user-login"),

    # Worklist
    path("api/get-tasks/<int:user_id>",AllTaskView.as_view(), name="get-all-tasks"),
    path("api/get-task/<int:id>", TaskView.as_view(), name="get-task"),
    path("api/update-task/<int:id>", TaskView.as_view(), name="update-task"),
    path("api/add-task/", AllTaskView.as_view(), name="add-task"),
    path("api/delete-task/<int:id>", TaskView.as_view(), name="delete-task"),

    #dashboard
    path("api/dashboard/<int:user_id>", Dashboard.as_view(), name="dashboard"),

]