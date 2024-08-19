from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from tasks.models import Employee, Task
from tasks.validators import DeadlineValidator, NameValidator


class EmployeeSerializer(ModelSerializer):
    """
    Сериализатор сотрудника.
    """

    class Meta:
        model = Employee
        fields = "__all__"
        validators = [
            NameValidator(
                field="name",
            ),
        ]


class BusyEmployeeListSerializer(ModelSerializer):
    """
    Сериализатор списка занятых сотрудников.
    """

    tasks = SerializerMethodField()
    task_count = SerializerMethodField()

    class Meta:
        model = Employee
        fields = "__all__"
        validators = [
            NameValidator(
                field="name",
            ),
        ]

    def get_tasks(self, employee):
        """
        Возвращает список активных заданий сотрудника.
        """
        return [
            task.title
            for task in Task.objects.filter(executor=employee, status="IN_PROGRESS")
        ]

    def get_task_count(self, employee):
        """
        Возвращает количество активных заданий сотрудника.
        """
        return Task.objects.filter(executor=employee, status="IN_PROGRESS").count()


class TaskSerializer(ModelSerializer):
    """
    Сериализатор задачи.
    """

    class Meta:
        model = Task
        fields = "__all__"
        validators = [
            DeadlineValidator(field="deadline"),
        ]
        read_only_fields = ("status",)


class TaskUpdateSerializer(ModelSerializer):
    """
    Сериализатор изменения задачи.
    """

    class Meta:
        model = Task
        fields = "__all__"
        validators = [
            DeadlineValidator(field="deadline"),
        ]


class ImportantTaskSerializer(ModelSerializer):
    """
    Сериализатор важной задачи.
    """

    possible_executors = SerializerMethodField()

    class Meta:
        model = Task
        fields = ("title", "deadline", "possible_executors")

    def get_possible_executors(self, task):
        """
        Возвращает имена сотрудников, кому можно назначить
        задачу, не взятую в работу.
        """

        # Получаем сотрудников с наименьшим количеством задач на исполнении
        employees = Employee.objects.all()
        employees_task_count = {}
        for employee in employees:
            employees_task_count[employee.name] = employee.tasks.count()

        min_task_count = min(employees_task_count.values())
        possible_executors = [
            employee
            for employee in employees_task_count
            if employees_task_count[employee] == min_task_count
        ]

        # Получаем количество задач исполнителя зависимой задачи
        dependent_task = Task.objects.get(parent_task=task)
        current_executor = dependent_task.executor
        current_task_count = current_executor.tasks.count()

        # Добавляем к списку исполнителя зависимой задачи, если его нет в списке,
        # и ему назначено максимум на 2 задачи больше, чем у наименее загруженного сотрудника

        if current_executor not in possible_executors:
            if current_task_count <= min_task_count + 2:
                possible_executors.append(current_executor.name)

        return possible_executors
