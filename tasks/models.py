from django.db import models

NULLABLE = {"blank": True, "null": True}


class Employee(models.Model):
    """
    Модель сотрудника.
    """
    name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Должность")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["name"]

    def __str__(self):
        return f'{self.name} ({self.position})'


class Task(models.Model):
    """
    Модель задачи.
    """
    STATUS_CHOICES = [
        ("NEW", "Новая"),
        ("IN_PROGRESS", "В процессе"),
        ("DONE", "Завершена"),
    ]

    title = models.CharField(max_length=255, verbose_name="Наименование")
    parent_task = models.ForeignKey('self', **NULLABLE, on_delete=models.CASCADE, verbose_name="Родительская задача")
    executor = models.ForeignKey(Employee, **NULLABLE, on_delete=models.SET_NULL, verbose_name="Исполнитель", related_name="tasks")
    deadline = models.DateField(verbose_name="Срок исполнения")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="NEW", verbose_name="Статус задачи"
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-deadline"]

    def __str__(self):
        return f'{self.title} до {self.deadline} ({self.status})'
