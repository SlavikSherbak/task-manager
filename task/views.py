from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from django.urls import reverse_lazy
from django.views import generic

from task.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
    ProjectForm,
    TeamForm,
    TaskUpdateForm,
    TaskCreateForm,
)
from django.contrib.auth import logout

from task.models import (
    Project,
    Task,
    Worker,
    Team,
    Position,
    TaskType,
    Priority
)


class ProjectsListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "projects_list"
    template_name = "pages/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.exclude(is_completed=True)

        context["tasks"] = tasks
        context["segment"] = "index"
        return context


class ProjectsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs
        for key, value in pk.items():
            pk = value
        project = Project.objects.get(pk=pk)

        tasks = Task.objects.filter(project=project.id)

        context["tasks"] = tasks
        context["segment"] = "tables"
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task:index")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task:index")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task:index")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.object.project.id
        return kwargs


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:index")


@login_required
def toggle_mark_completed(request, pk, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not task.is_completed:
        task.is_completed = True
        task.save()
    return HttpResponseRedirect(reverse_lazy("task:project-detail", args=[pk]))


@login_required
def toggle_assign_to_task(request, pk, task_id):
    worker = Worker.objects.get(pk=request.user.id)
    task = Task.objects.get(pk=task_id)
    if worker in task.assignees.all():
        task.assignees.remove(worker)
    else:
        task.assignees.add(worker)
    return HttpResponseRedirect(reverse_lazy("task:project-detail", args=[pk]))


@login_required
def toggle_remove_worker_from_team(request, pk, team_id):
    team = Team.objects.get(pk=team_id)
    worker = Worker.objects.get(pk=pk)
    team.team.remove(worker)
    return HttpResponseRedirect(reverse_lazy("task:team-list"))


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "team_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["segment"] = "team"
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task:team-list")

    def get_initial(self):
        initial = super().get_initial()
        team = self.get_object()
        workers = team.team.all()
        initial["worker"] = workers
        return initial


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task:team-list")


class AdditionalParametersListView(LoginRequiredMixin, generic.ListView):
    model = Priority
    template_name = "task/additional-parameters.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["task_types"] = TaskType.objects.all()
        context["positions"] = Position.objects.all()
        context["segment"] = "additional-parameters"
        return context


class PriorityCreateView(LoginRequiredMixin, generic.CreateView):
    model = Priority
    fields = "__all__"
    success_url = reverse_lazy("task:additional-parameters")


class PriorityUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Priority
    fields = "__all__"
    success_url = reverse_lazy("task:additional-parameters")


class PriorityDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Priority
    success_url = reverse_lazy("task:additional-parameters")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:additional-parameters")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:additional-parameters")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task:additional-parameters")


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task:additional-parameters")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task:additional-parameters")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task:additional-parameters")


@login_required
def profile(request):
    projects = Project.objects.all()
    tasks = Task.objects.filter(
        assignees__username__contains=request.user.username
    )

    context = {
        "tasks": tasks,
        "projects": projects,
        "segment": "profile",
    }
    return render(request, "pages/profile.html", context=context)


# Authentication
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect("/accounts/login/")
        else:
            print("Register failed!")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy("task:login"))


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("task:profile")


class WorkerProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position")
    template_name = "task/user_profile.html"
    success_url = reverse_lazy("task:profile")

    def get_object(self, queryset=None):
        return self.request.user
