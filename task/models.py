from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self) -> str:
        return (
            f"{self.username} "
            f"({self.first_name} {self.last_name})"
            f" position {self.position.name}"
        )


class Priority(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks"
    )

    def __str__(self) -> str:
        return f"{self.name}, is completed {self.is_completed}"


class Team(models.Model):
    name = models.CharField(max_length=64, default="New team")
    team = models.ManyToManyField(
        Worker,
        related_name="teams"
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Project(models.Model):
    name = models.CharField(max_length=64, unique=True)
    tasks = models.ManyToManyField(
        Task,
        related_name="projects"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.name}"
