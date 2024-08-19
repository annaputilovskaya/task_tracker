from django.db.models import Count
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from tasks.models import Employee, Task
from tasks.paginations import CustomPagination
from tasks.serializers import (EmployeeSerializer, ImportantTaskSerializer,
                               TaskSerializer, TaskUpdateSerializer)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер постраничного вывода списка сотрудников, "
        "отсортированных по количеству активных задач, "
        "с указанием количества активных задач."
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Контроллер просмотра информации по сотруднику."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Контроллер создания сотрудника."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер изменения сотрудника."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Контроллер удаления сотрудника."
    ),
)
class EmployeeViewSet(ModelViewSet):
    """
    Контроллер модели сотрудника.
    """

    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает список сотрудников,
        отсортированный по количеству их активных задач
        """
        queryset = (
            Employee.objects.all()
            .annotate(task_count=Count("tasks"))
            .order_by("task_count")
        )
        return queryset


class TaskCreateAPIView(CreateAPIView):
    """
    Создание новой задачи.
    """

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        """
        Сохраняет новую задачу и
        устанавливает статус "В работе" при назначении исполнителя
        """
        new_task = serializer.save()
        if new_task.executor:
            new_task.status = "IN_PROGRESS"
        new_task.save()


class TaskListAPIView(ListAPIView):
    """
    Получение списка всех задач.
    """

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination


class ImportantTaskListAPIView(ListAPIView):
    """
    Получение списка важных задач, не взятых в работу, в формате:
    {<Важная задача>, <Срок>, [<ФИО сотрудников, кому можно назначить задачу>]}
    """

    serializer_class = ImportantTaskSerializer

    def get_queryset(self):
        """
        Возвращает перечень важных задач, не взятых в работу
        """
        important_tasks = []
        dependent_tasks = Task.objects.exclude(parent_task=None).filter(
            status="IN_PROGRESS", parent_task__status="NEW"
        )
        for task in dependent_tasks:
            important_tasks.append(task.parent_task)
        return important_tasks


class TaskRetrieveAPIView(RetrieveAPIView):
    """
    Получение информации о конкретной задаче.
    """

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (AllowAny,)


class TaskUpdateAPIView(UpdateAPIView):
    """
    Изменение информации о задаче.
    """

    serializer_class = TaskUpdateSerializer
    queryset = Task.objects.all()

    def perform_update(self, serializer):
        """
        Если при изменении задачи назначается исполнитель,
        устанавливает статус "В работе".
        """
        task = serializer.save()
        if task.executor and task.status == "NEW":
            task.status = "IN_PROGRESS"
        task.save()


class TaskDestroyAPIView(DestroyAPIView):
    """
    Удаление задачи.
    """

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
