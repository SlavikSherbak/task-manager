from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    UsernameField,
    PasswordResetForm,
    SetPasswordForm,
)
from django.utils.translation import gettext_lazy as _

from task.models import Worker, Project, Task, Team

PRIORITY_CHOICES = (
    ("Urgent", "Urgent"),
    ("High", "High"),
    ("Middle", "Middle"),
    ("low", "low"),
)


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password Confirmation"}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("username", "email", "position")

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "position": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        ),
        label="Confirm New Password",
    )


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Old Password"}
        ),
        label="Old Password",
    )
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        ),
        label="Confirm New Password",
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["tasks"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team"].queryset = Team.objects.filter(team=user)


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )


class TaskUpdateForm(forms.ModelForm):
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    deadline = forms.DateTimeField(widget=DateTimeInput)
    assignees = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label="Assignees",
        required=False,
    )

    class Meta:
        model = Task
        exclude = ["is_completed", "project"]
        widgets = {"deadline": DateTimeInput()}

    def __init__(self, project, *args, **kwargs):
        project = Project.objects.get(id=project)
        super().__init__(*args, **kwargs)
        self.fields["assignees"].queryset = Worker.objects.filter(teams=project.team)


class TaskCreateForm(forms.ModelForm):
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    deadline = forms.DateTimeField(widget=DateTimeInput)

    class Meta:
        model = Task
        exclude = ["is_completed", "assignees"]
        widgets = {"deadline": DateTimeInput()}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(team__team=user)


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title..."})
    )


class TeamForm(forms.ModelForm):
    team = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Team
        fields = "__all__"
