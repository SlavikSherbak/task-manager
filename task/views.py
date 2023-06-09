from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
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
    TaskSearchForm,
    ProjectSearchForm,
)
from django.contrib.auth import logout

from task.models import (
    Project,
    Task,
    Worker,
    Team,
    Position,
    TaskType,
)


class ProjectsListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "projects_list"
    template_name = "pages/index.html"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ProjectSearchForm(
            initial={"name": name}
        )

        context["segment"] = "index"
        return context

    def get_queryset(self):
        username = self.request.user.username

        queryset = (
            Project.objects.select_related("team")
            .filter(team__team__username=username)
        )
        form = ProjectSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task:index")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        project = Project.objects.get(pk=self.kwargs["pk"])
        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )

        self.get_queryset().filter(project=project)

        context["project"] = project
        context["segment"] = "tables"
        return context

    def get_queryset(self) -> QuerySet:
        queryset = (
            Task.objects.select_related("task_type").
            select_related("project")
            .filter(project=self.kwargs["pk"], is_completed=False)
        )
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
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
    return HttpResponseRedirect(reverse_lazy("task:task-list", args=[pk]))


@login_required
def toggle_assign_to_task(request, pk, task_id):
    worker = Worker.objects.get(pk=request.user.id)
    task = Task.objects.get(pk=task_id)
    if worker in task.assignees.all():
        task.assignees.remove(worker)
    else:
        task.assignees.add(worker)
    return HttpResponseRedirect(reverse_lazy("task:task-list", args=[pk]))


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
    model = Position
    template_name = "task/additional-parameters.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["task_types"] = TaskType.objects.all()
        context["segment"] = "additional-parameters"
        return context


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


class UserAllTaskList(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 7
    template_name = "task/user_all_tasks.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )

        context["segment"] = "user_tasks"
        return context

    def get_queryset(self):
        queryset = (
            Task.objects.select_related("task_type")
            .select_related("project")
            .filter(assignees=self.request.user)
        )

        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


@login_required
def profile(request):
    projects = Project.objects.all()
    tasks = (
        Task.objects.filter(
            assignees__username__contains=request.user.username
        )
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
