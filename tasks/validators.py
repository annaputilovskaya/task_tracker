import re

from django.utils import timezone
from rest_framework.serializers import ValidationError


class NameValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('^[А-ЯЁ]{1}[а-яё]{0,}[\s-]{1}(?:[А-Яа-яЁё]{1}[а-яё]{0,}[\s-]{1}){0,}[А-Яа-яЁё]{1}[а-яё]{0,}+$')
        tmp_name = dict(value).get(self.field)
        if not bool(reg.match(tmp_name)):
            raise ValidationError(
                "Фамилия, имя и отчетсво могут содержать только буквы кириллицы и дефисы. "
                "Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества."
                )


class DeadlineValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        deadline = dict(value).get(self.field)
        if deadline and deadline < timezone.now().date():
            raise ValidationError("Срок исполнения должен быть больше текущей даты.")
        related_task = value.get("related_task")
        if related_task and deadline < related_task.deadline:
            raise ValidationError("Срок исполнения задачи не может быть меньше срока исполнения связанной задачи.")
