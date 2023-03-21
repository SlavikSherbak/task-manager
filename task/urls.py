from django.urls import path

from task.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "task"
