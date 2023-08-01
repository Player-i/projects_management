from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import (
    EmailLoginForm,
    UserRegistrationForm,
    StepForm,
    ProjectForm,
    ManagerCreatesUserForm,
    StepDoneForm,
)
from django.contrib.auth import authenticate, login, logout
from .models import Project, Step
from django import forms
from .models import MyUser
from django.forms import modelformset_factory


# Create your views here.


def home(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_project_manager:
            projects = (
                Project.objects.filter(author=user)
                .prefetch_related("step_set")
                .order_by("-id")  # Reverse order by project ID
                .all()
            )
        else:
            manager = MyUser.objects.get(email=user.manager)
            projects = (
                Project.objects.filter(author=manager)
                .prefetch_related("step_set")
                .order_by("-id")  # Reverse order by project ID
                .all()
            )
        context["projects"] = projects
        context["user"] = user
        return render(request, "home.html", context=context)
    else:
        return redirect("login")


def create_users(request):
    user = request.user
    if request.method == "POST":
        form = ManagerCreatesUserForm(request.POST)
        if form.is_valid():
            # Create the new user without using the form's save() method
            new_user = MyUser(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                manager=user.email,  # Set the manager for the new user
            )
            new_user.set_password(form.cleaned_data["password1"])
            new_user.save()  # Redirect to the same page after user creation
    else:
        form = ManagerCreatesUserForm()
    # Fetch non-project manager users
    return render(request, "create_users.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or perform any other desired actions
                return redirect("home")  # Replace 'home' with your desired URL name
            else:
                # Authentication failed
                form.add_error(None, "Invalid email or password.")
    else:
        form = EmailLoginForm()

    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user yet
            user.is_project_manager = True  # Set the user as a project manager
            user.save()  # Now save the user with the updated is_project_manager field
            return redirect("login")  # Name used in urls.py
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "register.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def step_details(request, step_id):
    context = {}

    step = get_object_or_404(Step, id=step_id)

    # Get the project ID from the related Project object
    project_id = step.project.id

    # Create an instance of the StepDoneForm with the current step's data
    step_done_form = StepDoneForm(instance=step)

    if request.method == "POST":
        # Check if the user submitted the StepDoneForm
        if "step_done_form" in request.POST:
            step_done_form = StepDoneForm(request.POST, instance=step)
            if step_done_form.is_valid():
                step_done_form.save()
                # Redirect to the project_details page with the project_id in the URL
                return redirect("project_details", project_id=project_id)

    context["step"] = step
    context["step_done_form"] = step_done_form
    context["project_id"] = project_id  # Pass the project ID to the template
    return render(request, "step_details.html", context)


def create_project(request):
    user = request.user
    users = MyUser.objects.filter(manager=user.email)
    StepFormSet = forms.formset_factory(
        form=StepForm, extra=0, min_num=1
    )  # min_num is set to 1 to have at least one step
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        formset = StepFormSet(request.POST, prefix="steps")
        print(formset)

        if project_form.is_valid() and formset.is_valid():
            project = project_form.save(commit=False)

            # Set the author (manager) to the currently logged-in user
            project.author = request.user
            print(project.author)

            # Save the project to the database with the author assigned
            project.save()

            for form in formset:
                step = form.save(commit=False)
                step.project = project
                assigned_to = form.cleaned_data.get(
                    "assigned_to"
                )  # Get the value from the dropdown
                step.assigned_to = assigned_to
                step.save()

            return redirect("home")  # Redirect to home page
    else:
        project_form = ProjectForm()
        formset = StepFormSet(prefix="steps")  # Queryset is set to an empty list

    total_form_count = formset.total_form_count()  # Calculate total form count
    return render(
        request,
        "create_project.html",
        {
            "project_form": project_form,
            "formset": formset,
            "users": users,
            "total_form_count": total_form_count,  # Pass total form count to the template
        },
    )


def project_details(request, project_id):
    context = {}
    user = request.user
    context["user"] = user

    # Get the project instance using the project_id from the URL
    project = get_object_or_404(Project, id=project_id)

    # Fetch the steps associated with the project
    steps = project.step_set.all()

    context["project"] = project
    context["steps"] = steps

    return render(request, "project_details.html", context)
