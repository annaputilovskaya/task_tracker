from django.urls import path
from rest_framework.routers import SimpleRouter

from tasks.apps import TasksConfig
from tasks.views import (EmployeeViewSet, ImportantTaskListAPIView,
                         TaskCreateAPIView, TaskDestroyAPIView,
                         TaskListAPIView, TaskRetrieveAPIView,
                         TaskUpdateAPIView)

app_name = TasksConfig.name

router = SimpleRouter()
router.register("employees", EmployeeViewSet, basename="employees")

urlpatterns = [
    path("create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("", TaskListAPIView.as_view(), name="tasks"),
    path("important/", ImportantTaskListAPIView.as_view(), name="important-tasks"),
    path("<int:pk>/", TaskRetrieveAPIView.as_view(), name="task"),
    path("<int:pk>/update/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task-delete"),
]

urlpatterns += router.urls
