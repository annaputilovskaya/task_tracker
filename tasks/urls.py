from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import (BusyEmployeeListAPIView, EmployeeCreateAPIView,
                         EmployeeDestroyAPIView, EmployeeListAPIView,
                         EmployeeRetrieveAPIView, EmployeeUpdateAPIView,
                         ImportantTaskListAPIView, TaskCreateAPIView,
                         TaskDestroyAPIView, TaskListAPIView,
                         TaskRetrieveAPIView, TaskUpdateAPIView)

app_name = TasksConfig.name

urlpatterns = [
    path("employees/create", EmployeeCreateAPIView.as_view(), name="employee-create"),
    path("employees/", EmployeeListAPIView.as_view(), name="employees"),
    path("employees/busy/", BusyEmployeeListAPIView.as_view(), name="busy-employees"),
    path("employees/<int:pk>/", EmployeeRetrieveAPIView.as_view(), name="employee"),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateAPIView.as_view(),
        name="employee-update",
    ),
    path(
        "employees/<int:pk>/delete/",
        EmployeeDestroyAPIView.as_view(),
        name="employee-delete",
    ),
    path("create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("", TaskListAPIView.as_view(), name="tasks"),
    path("important/", ImportantTaskListAPIView.as_view(), name="important-tasks"),
    path("<int:pk>/", TaskRetrieveAPIView.as_view(), name="task"),
    path("<int:pk>/update/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task-delete"),
]
