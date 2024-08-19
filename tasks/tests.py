from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Employee, Task
from users.models import User


class EmployeeTestCase(APITestCase):
    """
    Класс тестов модели Сотрудника.
    """

    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")
        self.employee1 = Employee.objects.create(
            name="Первый Тестовый Сотрудник", position="Тестовая1"
        )

    def test_str_habit(self):
        """
        Тестирует строчное представление сотрудника.
        """
        employee = Employee.objects.get(pk=self.employee1.pk)
        self.assertEqual(str(employee), f"{employee.name} ({employee.position})")

    def test_employee_retrieve_unauthenticated_user(self):
        """
        Тестирует просмотр сотрудника без аутентификации.
        """
        url = reverse("tasks:employees-detail", args=(self.employee1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.employee1.name)
        self.assertEqual(data.get("position"), self.employee1.position)

    def test_employee_retrieve_authenticated_user(self):
        """
        Тестирует просмотр сотрудника аутентифиуировнным пользователем.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse("tasks:employees-detail", args=(self.employee1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.employee1.name)
        self.assertEqual(data.get("position"), self.employee1.position)

    def test_employee_create_unauthenticated_user(self):
        """
        Тестирует создание нового сотрудника без аутнентификации.
        """
        url = reverse("tasks:employees-list")
        data = {
            "name": "Второй тестовый сотрудник",
            "position": "Тестовая2",
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_create_authenticated_user(self):
        """
        Тестирует создание нового сотрудника аутентифиуировнным пользователем.
        """

        url = reverse("tasks:employees-list")
        data = [
            {
                "name": "Второй тестовый Сотрудник",
                "position": "Тестовая2",
            },
            {
                "name": "Третий тестовый",
                "position": "Тестовая3",
            },
            {
                "name": "Четвертый-четвертый тестовый сотрудник",
                "position": "Тестовая4",
            },
            {
                "name": "Пятый-пятый тестовый Тестовый сотрудник-сотрудник",
                "position": "Тестовая5",
            },
            {
                "name": "Шестой",
                "position": "Тестовая6",
            },
            {
                "name": "седьмой Тестовый Сотрудник",
                "position": "Тестовая7",
            },
            {
                "name": "Восьмой8 тестовый сотрудник",
                "position": "Тестовая8",
            },
            {
                "name": "Nine Тестовый сотрудник",
                "position": "Тестовая9",
            },
            {
                "name": "Десятый тестовый? сотрудник",
                "position": "Тестовая10",
            },
            {
                "name": "Одиннадцатый- Тестовый сотрудник",
                "position": "Тестовая11",
            },
        ]

        self.client.force_authenticate(user=self.user1)

        # Тестируем создание пользователя с корректным именем
        response = self.client.post(url, data=data[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.get(position="Тестовая2"))

        response = self.client.post(url, data=data[1])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.get(position="Тестовая3"))

        response = self.client.post(url, data=data[2])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.get(position="Тестовая4"))

        response = self.client.post(url, data=data[3])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.get(position="Тестовая5"))

        # Тестируем создание пользователя с некорректным именем
        response = self.client.post(url, data=data[4])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
            ],
        )

        response = self.client.post(url, data=data[5])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
            ],
        )

        response = self.client.post(url, data=data[6])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
            ],
        )

        response = self.client.post(url, data=data[7])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
            ],
        )

        response = self.client.post(url, data=data[8])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
            ],
        )

        response = self.client.post(url, data=data[9])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
            ],
        )

    def test_employee_update_unauthenticated_user(self):
        """
        Тестирует изменение сотрудника без аутентификации.
        """
        url = reverse("tasks:employees-detail", args=(self.employee1.pk,))
        data = {"name": "Измененный тестовый сотрудник"}

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_update_authenticated_user(self):
        """
        Тестирует изменение сотрудника аутентифицировнным пользователем.
        """
        url = reverse("tasks:employees-detail", args=(self.employee1.pk,))
        data = [
            {"name": "Измененный тестовый сотрудник"},
            {"name": "Default измененный тестовый сотрудник"},
        ]

        self.client.force_authenticate(user=self.user1)

        # Тестируем изменение имени пользователя на корректное
        response = self.client.patch(url, data=data[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Измененный тестовый сотрудник")

        # Тестируем изменение имени пользователя на некорректное
        response = self.client.patch(url, data=data[1])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
            ],
        )

    def test_employee_delete_unauthenticated_user(self):
        """
        Тестирует удаление сотрудника без аутентификации.
        """
        url = reverse("tasks:employees-detail", args=(self.employee1.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Employee.objects.filter(pk=self.employee1.pk).exists())

    def test_employee_delete_authenticated_user(self):
        """
        Тестирует удаление сотрудника аутентифицировнным пользователем.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse("tasks:employees-detail", args=(self.employee1.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(pk=self.employee1.pk).exists())

    def test_employee_list_unauthenticated_user(self):
        """
        Тестирует получение списка сотрудников без аутентификации.
        """
        url = reverse("tasks:employees-list")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.employee1.pk,
                    "tasks": [],
                    "task_count": 0,
                    "name": self.employee1.name,
                    "position": self.employee1.position,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_employee_list_authenticated_user(self):
        """
        Тестирует получение списка сотрудников аутентифицировнным пользователем.
        """
        url = reverse("tasks:employees-list")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.employee1.pk,
                    "tasks": [],
                    "task_count": 0,
                    "name": self.employee1.name,
                    "position": self.employee1.position,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class TaskTestCase(APITestCase):
    """
    Класс тестов для модели Задачи.
    """

    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")
        self.employee1 = Employee.objects.create(
            name="Первый тестовый сотрудник", position="Должность"
        )
        self.employee2 = Employee.objects.create(
            name="Второй тестовый сотрудник", position="Должность"
        )
        self.employee3 = Employee.objects.create(
            name="Третий тестовый сотрудник", position="Должность"
        )
        self.employee4 = Employee.objects.create(
            name="Четвертый тестовый сотрудник", position="Должность"
        )
        self.task1 = Task.objects.create(
            title="Тестовая задача1", deadline="2025-01-01"
        )
        self.task2 = Task.objects.create(
            title="Тестовая задача2", deadline="2025-01-01"
        )
        self.task3 = Task.objects.create(
            title="Тестовая задача3", deadline="2025-01-01"
        )
        self.task4 = Task.objects.create(
            title="Тестовая задача4",
            deadline="2025-01-01",
            parent_task=self.task1,
            executor=self.employee1,
        )
        self.task5 = Task.objects.create(
            title="Тестовая задача5",
            deadline="2025-01-01",
            parent_task=self.task2,
            executor=self.employee1,
        )
        self.task6 = Task.objects.create(
            title="Тестовая задача6", deadline="2025-01-01", executor=self.employee2
        )

    def test_str_task(self):
        """
        Тестирует отображение строкового представления задачи.
        """
        task1 = Task.objects.get(pk=1)
        task2 = Task.objects.get(pk=6)
        self.assertEqual(
            str(self.task1), f"{task1.title} до {task1.deadline} ({task1.status})"
        )
        self.assertEqual(
            str(self.task6), f"{task2.title} до {task2.deadline} ({task2.status})"
        )

    def test_task_retrieve_unauthenticated_user(self):
        """
        Тестирует получение информации о задаче без аутентификации.
        """
        url = reverse("tasks:task", args=(self.task1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.task1.title)
        self.assertEqual(data.get("deadline"), self.task1.deadline)

    def test_task_retrieve_authenticated_user(self):
        """
        Тестирует получение информации о задаче аутентифицированным пользователем.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse("tasks:task", args=(self.task1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.task1.title)
        self.assertEqual(data.get("deadline"), self.task1.deadline)

    def test_task_create_unauthenticated_user(self):
        """
        Тестирует создание задачи без аутентификации.
        """
        url = reverse("tasks:task-create")
        data = {"title": "Тестовая задача7", "deadline": "2025-01-01"}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Task.objects.filter(pk=7).exists())

    def test_task_create_authenticated_user(self):
        """
        Тестирует создание задачи аутентифицированным пользователем.
        """
        url = reverse("tasks:task-create")
        data = [
            {"title": "Тестовая задача7", "deadline": "2025-01-01"},
            {
                "title": "Тестовая задача8",
                "deadline": "2025-01-01",
                "parent_task": self.task3.pk,
                "executor": self.employee1.pk,
            },
            {"title": "Тестовая задача9", "deadline": "2024-01-01"},
            {
                "title": "Тестовая задача8",
                "deadline": "2024-12-01",
                "parent_task": self.task1.pk,
                "executor": self.employee1.pk,
            },
        ]

        self.client.force_authenticate(user=self.user1)

        # Тестируем создание задачи с корректным сроком исполнения
        response = self.client.post(url, data=data[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(title="Тестовая задача7")
        self.assertEqual(task.status, "NEW")

        response = self.client.post(url, data=data[1])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(title="Тестовая задача8")
        self.assertEqual(task.status, "IN_PROGRESS")

        # Тестируем создание задачи с некорректным сроком исполнения
        response = self.client.post(url, data=data[2])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, data=data[3])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_update_unauthenticated_user(self):
        """
        Тестирует изменение задачи без аутентификации.
        """
        url = reverse("tasks:task-update", args=(self.task1.pk,))
        data = {"title": "Измененная тестовая задача1", "executor": self.employee2}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.get(pk=self.task1.pk).title, "Тестовая задача1")

    def test_task_update_authenticated_user(self):
        """
        Тестирует изменение задачи аутентифицированным пользователем.
        """

        url = reverse("tasks:task-update", args=(self.task1.pk,))
        data = [
            {"title": "Измененная тестовая задача1", "executor": self.employee2.pk},
            {"title": "Измененная тестовая задача1", "status": "DONE"},
            {"title": "Измененная тестовая задача1", "deadline": "2024-01-01"},
            {
                "title": "Измененная тестовая задача1",
                "deadline": "2024-12-01",
                "parent_task": self.task1.pk,
            },
        ]

        self.client.force_authenticate(user=self.user1)

        # Тестируем изменение задачи с корректными данными
        response = self.client.patch(url, data=data[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(task.title, "Измененная тестовая задача1")
        self.assertEqual(task.status, "IN_PROGRESS")

        response = self.client.patch(url, data=data[1])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(task.title, "Измененная тестовая задача1")
        self.assertEqual(task.status, "DONE")

        # Тестируем изменение задачи с некорректными данными
        response = self.client.patch(url, data=data[2])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(url, data=data[3])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_delete_unauthenticated_user(self):
        """
        Тестирует удаление задачи без аутентификации.
        """
        url = reverse("tasks:task-delete", args=(self.task1.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())

    def test_task_delete_authenticated_user(self):
        """
        Тестирует удаление задачи аутентифицированным пользователем.
        """
        url = reverse("tasks:task-delete", args=(self.task1.pk,))

        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_task_list_unauthenticated_user(self):
        """
        Тестирует получение списка задач без аутентификации.
        """
        url = reverse("tasks:tasks")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 6,
            "next": "http://testserver/?page=2",
            "previous": None,
            "results": [
                {
                    "id": self.task1.pk,
                    "title": self.task1.title,
                    "deadline": self.task1.deadline,
                    "status": self.task1.status,
                    "parent_task": None,
                    "executor": None,
                },
                {
                    "id": self.task2.pk,
                    "title": self.task2.title,
                    "deadline": self.task2.deadline,
                    "status": self.task2.status,
                    "parent_task": None,
                    "executor": None,
                },
                {
                    "id": self.task3.pk,
                    "title": self.task3.title,
                    "deadline": self.task3.deadline,
                    "status": self.task3.status,
                    "parent_task": None,
                    "executor": None,
                },
                {
                    "id": self.task4.pk,
                    "title": self.task4.title,
                    "deadline": self.task4.deadline,
                    "status": self.task4.status,
                    "parent_task": self.task4.parent_task.pk,
                    "executor": self.task4.executor.pk,
                },
                {
                    "id": self.task5.pk,
                    "title": self.task5.title,
                    "deadline": self.task5.deadline,
                    "status": self.task5.status,
                    "parent_task": self.task5.parent_task.pk,
                    "executor": self.task5.executor.pk,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_task_list_authenticated_user(self):
        """
        Тестирует получение списка задач аутентифицированным пользователем.
        """
        url = reverse("tasks:tasks")

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 6,
            "next": "http://testserver/?page=2",
            "previous": None,
            "results": [
                {
                    "id": self.task1.pk,
                    "title": self.task1.title,
                    "deadline": self.task1.deadline,
                    "status": self.task1.status,
                    "parent_task": None,
                    "executor": None,
                },
                {
                    "id": self.task2.pk,
                    "title": self.task2.title,
                    "deadline": self.task2.deadline,
                    "status": self.task2.status,
                    "parent_task": None,
                    "executor": None,
                },
                {
                    "id": self.task3.pk,
                    "title": self.task3.title,
                    "deadline": self.task3.deadline,
                    "status": self.task3.status,
                    "parent_task": None,
                    "executor": None,
                },
                {
                    "id": self.task4.pk,
                    "title": self.task4.title,
                    "deadline": self.task4.deadline,
                    "status": self.task4.status,
                    "parent_task": self.task4.parent_task.pk,
                    "executor": self.task4.executor.pk,
                },
                {
                    "id": self.task5.pk,
                    "title": self.task5.title,
                    "deadline": self.task5.deadline,
                    "status": self.task5.status,
                    "parent_task": self.task5.parent_task.pk,
                    "executor": self.task5.executor.pk,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
