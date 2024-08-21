from django.contrib import admin

from tasks.models import Employee, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "position")
    list_filter = ("position",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent_task", "status", "executor", "deadline")
    list_filter = ("status", "executor")
    search_fields = ("title", "parent_task")
    order_by = ("-deadline",)
