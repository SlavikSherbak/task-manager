from django.urls import path
from task import views
from django.contrib.auth import views as auth_views

from task.views import (
    ProjectsListView, ProjectsDetailView, ProjectCreateView,
    ProjectUpdateView, ProjectDeleteView, toggle_mark_completed,
    toggle_assign_to_task, TaskDeleteView, TaskUpdateView,
    TaskCreateView, TeamUpdateView, TeamDeleteView, TeamListView,
    toggle_remove_worker_from_team, TeamCreateView, AdditionalParametersListView,
    PriorityCreateView, PriorityUpdateView, PriorityDeleteView,
    PositionCreateView, PositionUpdateView, PositionDeleteView,
    TaskTypeDeleteView, TaskTypeUpdateView, TaskTypeCreateView,
    WorkerProfileUpdateView
)


urlpatterns = [
    path("", ProjectsListView.as_view(), name="index"),
    path("project/create/", ProjectCreateView.as_view(), name="project-create"),
    path("project/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
    path("project/<int:pk>/", ProjectsDetailView.as_view(), name="project-detail"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "project/<int:pk>/task/<int:task_id>/toggle-assign-status/",
        toggle_mark_completed,
        name="toggle_mark_completed",
    ),
    path(
        "project/<int:pk>/task/<int:task_id>/toggle-assign-task/",
        toggle_assign_to_task,
        name="toggle_assign_to_task",
    ),
    path(
        "team<int:pk>/team/<int:team_id>/toggle-remove_worker/",
        toggle_remove_worker_from_team,
        name="toggle_remove_worker_from_team",
    ),
    path("team/", TeamListView.as_view(), name="team-list"),
    path("team/create", TeamCreateView.as_view(), name="team-create"),
    path("team/<int:pk>/update", TeamUpdateView.as_view(), name="team-update"),
    path("team/<int:pk>/delete", TeamDeleteView.as_view(), name="team-delete"),
    path("additional-parameters/", AdditionalParametersListView.as_view(), name="additional-parameters"),
    path("priority/create", PriorityCreateView.as_view(), name="priority-create"),
    path("priority/<int:pk>/update", PriorityUpdateView.as_view(), name="priority-update"),
    path("priority/<int:pk>/delete", PriorityDeleteView.as_view(), name="priority-delete"),

    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
