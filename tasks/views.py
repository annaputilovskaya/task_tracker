from django.db.models import Count
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from tasks.models import Employee, Task
from tasks.paginations import CustomPagination
from tasks.serializers import (BusyEmployeeListSerializer, EmployeeSerializer,
                               ImportantTaskSerializer, TaskSerializer,
                               TaskUpdateSerializer)


class EmployeeCreateAPIView(CreateAPIView):
    """
    Контроллер создания сотрудника.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeListAPIView(ListAPIView):
    """
    Контроллер постраничного вывода списка сотрудников.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)


class BusyEmployeeListAPIView(ListAPIView):
    """
    Контроллер постраничного вывода списка сотрудников,
    отсортированных по количеству их активных задач
    с указанием количества активных задач.
    """

    queryset = Employee.objects.all()
    serializer_class = BusyEmployeeListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        self.queryset = Employee.objects.all()
        self.queryset = self.queryset.select_related()
        self.queryset = Employee.objects.annotate(tasks_count=Count("tasks")).order_by(
            "-tasks_count"
        )
        return self.queryset


class EmployeeRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер просмотра информации по сотруднику.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)


class EmployeeUpdateAPIView(UpdateAPIView):
    """
    Контроллер изменения сотрудника.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDestroyAPIView(DestroyAPIView):
    """
    Контроллер удаления сотрудника.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


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
