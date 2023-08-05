from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser, Step, Project
from django.contrib.auth import authenticate


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "due_date"]


class StepForm(forms.ModelForm):
    assigned_to = forms.CharField(max_length=100)

    class Meta:
        model = Step
        fields = ["name", "description", "due_date", "file"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class StepDoneForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ["is_done"]


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ["username", "email", "password1", "password2"]


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"autofocus": True})


class ManagerCreatesUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ["username", "email", "password1", "password2"]
