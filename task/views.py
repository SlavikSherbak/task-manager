from django.shortcuts import render

from task.models import Worker


def index(request):

    num_worker = Worker.objects.count()

    context = {
        "num_worker": num_worker,
    }

    return render(request, "task/index.html", context=context)
