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
    JobForm,
    BudgetForm
)
from django.contrib.auth import authenticate, login, logout
from .models import Project, Step
from django import forms
from .models import MyUser, Job, Budget
from django.forms import modelformset_factory
from django.forms.models import model_to_dict

# Create your views here.


def landing_page(request):
    return render(request, "landing_page.html")

def home(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_project_manager:
            jobs = (
                Job.objects.filter(author=user)
                .order_by("-id")  # Reverse order by project ID
                .all()
            )
            projects = (
                Project.objects.filter(author=user)
                .order_by("-id")  # Reverse order by project ID
                .all()
            )
        else:
            manager = MyUser.objects.get(email=user.manager)
            projects = (
                Project.objects.filter(
                    step__assigned_to=user.username,  # Filter projects based on steps assigned to the user
                    step__project__author=manager,  # Additionally, the project's author must be the user's manager
                )
                .distinct()
                .prefetch_related("step_set")
                .order_by("-id")
            )
        context["projects"] = projects
        context["jobs"] = jobs
        context["user"] = user
        return render(request, "home.html", context=context)
    else:
        return redirect("login")



def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # Don't save the user yet
            job.author = request.user  # Set the author to the currently logged-in user
            job.save() 
            return redirect("job_details", job_id= job.id)

    else: 
        job_form = JobForm()


    return render(request, "create_job.html", {"job_form": job_form})

def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    try:
        project = Project.objects.get(job=job)
    except Project.DoesNotExist:
        project = None

    # Check if a budget exists for the job
    try:
        # Check if a budget exists for the job
        budgets = Budget.objects.filter(job=job)

        # If there are multiple budgets, you may want to choose one or handle it accordingly
        budget = budgets.first()
    except Budget.DoesNotExist:
        budget = None

    return render(request, 'job_details.html', {'job': job, 'project': project, 'budget': budget})

def delete_job(request, job_id):
    # Check if the user is authenticated and a manager
    if request.user.is_authenticated and request.user.is_project_manager:
        job = get_object_or_404(Job, id=job_id)
        
        # Perform any additional logic before deleting, if needed
        
        job.delete()
        
        return redirect('home')


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
            return redirect("home")
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
    user = request.user
    context = {}

    step = get_object_or_404(Step, id=step_id)

    # Get the project ID from the related Project object
    project_id = step.project.id

    # Create an instance of the StepDoneForm with the current step's data
    step_done_form = StepDoneForm(instance=step)

    if request.method == "POST":
        # Check if the user submitted the StepDoneForm

        if "step_done_form" in request.POST:
            step_done_form = StepDoneForm(request.POST, request.FILES, instance=step)
            if step_done_form.is_valid():
                step_done_form.save()
                return redirect("project_details", project_id=project_id)

    context["user"] = user
    context["step"] = step
    context["step_done_form"] = step_done_form
    context["project_id"] = project_id  # Pass the project ID to the template
    return render(request, "step_details.html", context)

def create_budget(request, job_id):
    job = Job.objects.get(pk=job_id)

    if request.method == 'POST':
        # Get the existing budget instance or create a new one
        budget_instance, created = Budget.objects.get_or_create(job=job)

        # Iterate over POST data and update the budget fields
        # Iterate over the keys in request.POST and update the budget fields
        # Iterate over the keys in request.POST and update the budget fields
        for key, value in request.POST.items():
            if key not in ['csrfmiddlewaretoken', 'job', 'materials', 'labor', 'equipment', 'subcontract', 'other']:
                # Extract field name and type from the key
                
                field_name, field_type = key.rsplit('_', 1)

                # Check if the field type is valid (materials, labor, equipment, subcontract, other)
                if field_type in ['materials', 'labor', 'equipment', 'subcontract', 'other']:
                    # Convert the value to an integer if possible, default to 0
                    field_value = int(value) if value.isdigit() else 0

                    field = getattr(budget_instance, field_name)
                    field[field_type] = field_value

        # Save the changes to the budget instance
        budget_instance.initial_budget = True
        budget_instance.save()

        # Duplicate Budget
        budget_instance.pk = None
        budget_instance.initial_budget = False
        budget_instance.save()

        # Redirect to the appropriate page
        return redirect('job_details', job_id= job_id)

    return render(request, 'create_budget.html', {'job': job})

def edit_budget(request, job_id):
    
    job = get_object_or_404(Job, pk=job_id)


    if request.method == 'POST':
    # Get the existing budget instance or create a new one
        budget_instance = Budget.objects.filter(job=job, initial_budget=False).first()

    # Iterate over POST data and update the budget fields
    # Iterate over the keys in request.POST and update the budget fields
    # Iterate over the keys in request.POST and update the budget fields
        for key, value in request.POST.items():
            if key not in ['csrfmiddlewaretoken', 'job', 'materials', 'labor', 'equipment', 'subcontract', 'other']:
                # Extract field name and type from the key
                
                field_name, field_type = key.rsplit('_', 1)

                # Check if the field type is valid (materials, labor, equipment, subcontract, other)
                if field_type in ['materials', 'labor', 'equipment', 'subcontract', 'other']:
                    # Convert the value to an integer if possible, default to 0
                    field_value = int(value) if value.isdigit() else 0

                    field = getattr(budget_instance, field_name)
                    field[field_type] = field_value

        # Save the changes to the budget instance
        budget_instance.save()


        # Redirect to the appropriate page
        return redirect('job_details', job_id= job_id)

    # Get the job instance
    else:
    # Get the budget associated with the job where initial_budget is False
        budget = Budget.objects.filter(job=job, initial_budget=False).first()
        print(budget)
        budget_dict = model_to_dict(budget) if budget else {}
        # Your logic for handling the budget goes here

        return render(request, 'edit_budget.html', {'job': job, 'budget': budget_dict})


def initial_budget(request, job_id):
    
    job = get_object_or_404(Job, pk=job_id)



    # Get the budget associated with the job where initial_budget is False
    budget = Budget.objects.filter(job=job, initial_budget=True).first()
    print(budget)
    budget_dict = model_to_dict(budget) if budget else {}
    # Your logic for handling the budget goes here

    return render(request, 'initial_budget.html', {'job': job, 'budget': budget_dict})



def create_project(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user
    users = MyUser.objects.filter(manager=user.email)
    StepFormSet = forms.formset_factory(
        form=StepForm, extra=0, min_num=1
    )  # min_num is set to 1 to have at least one step
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        formset = StepFormSet(request.POST, request.FILES, prefix="steps")
        print(formset)

        if project_form.is_valid() and formset.is_valid():
            project = project_form.save(commit=False)

            # Set the author (manager) to the currently logged-in user
            project.job = job
            project.author = request.user

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

            return redirect("job_details", job_id=job.id)  # Redirect to home page
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


def edit_project(request, project_id):
    user = request.user
    users = MyUser.objects.filter(manager=user.email)
    project = get_object_or_404(Project, id=project_id)
    steps = project.step_set.all()
    job_id = project.job.id

    StepFormSet = forms.formset_factory(form=StepForm, extra=0, min_num=1)

    if request.method == "POST":
        project_form = ProjectForm(request.POST, instance=project)
        formset = StepFormSet(request.POST, request.FILES, prefix="steps")

        if project_form.is_valid() and formset.is_valid():
            project = project_form.save(commit=False)

            # Save the project to the database with the author assigned
            project.save()

            # Remove the first step from the queryset and delete it
            if steps.exists():
                first_step = steps.first()
                first_step.delete()

            for form in formset:
                step = form.save(commit=False)
                step.project = project
                assigned_to = form.cleaned_data.get("assigned_to")
                step.assigned_to = assigned_to
                step.save()

            return redirect("job_details", job_id=job_id)  # Redirect to the home page

    else:
        project_form = ProjectForm(instance=project)
        formset = StepFormSet(prefix="steps")

    total_form_count = formset.total_form_count()

    return render(
        request,
        "edit_project.html",
        {
            "project_form": project_form,
            "formset": formset,
            "users": users,
            "steps": steps,
            "total_form_count": total_form_count,
            "project": project,
        },
    )


def edit_step(request, step_id):
    user = request.user
    users = MyUser.objects.filter(manager=user.email)
    step = get_object_or_404(Step, id=step_id)

    if request.method == "POST":
        form = StepForm(request.POST, request.FILES, instance=step)
        if form.is_valid():
            step = form.save(commit=False)
            assigned_to = form.cleaned_data.get(
                "assigned_to"
            )  # Get the value from the dropdown
            step.assigned_to = assigned_to
            step.save()
            # Redirect to a success page or the step details page
            return redirect("step_details", step_id=step_id)
    else:
        form = StepForm(instance=step)

    return render(
        request, "edit_step.html", {"form": form, "step": step, "users": users}
    )


def delete_project(request, project_id):
    context = {}
    user = request.user
    context["user"] = user

    # Get the project instance using the project_id from the URL
    project = get_object_or_404(Project, id=project_id)
    context["project"] = project
    job_id = project.job.id

    if request.method == "POST":
        project.delete()
        # Redirect the user to a different page after deletion (you can customize this URL)
        return redirect("job_details", job_id=job_id)

    return render(request, "delete_project.html", context)


def duplicate_project(request, project_id):
    # Get the original project instance
    original_project = Project.objects.get(id=project_id)

    # Duplicate the project by creating a new instance
    new_project = Project.objects.create(
        name=f"{original_project.name} (Copy)",
        author=request.user,
        description=original_project.description,
        todays_date=original_project.todays_date,
        # Add any other fields you want to duplicate here
    )

    # Duplicate project steps
    for step in original_project.step_set.all():
        Step.objects.create(
            project=new_project,
            description=step.description,
            todays_date=step.todays_date,
            assigned_to=step.assigned_to,
            # Add any other fields you want to duplicate here
        )

    # Redirect the user to the newly duplicated project's details page
    return redirect("project_details", new_project.id)


def workers(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_project_manager:
            workers = MyUser.objects.filter(manager=user.email)
            projects = (
                Project.objects.filter(author=user)
                .prefetch_related("step_set")
                .order_by("-id")  # Reverse order by project ID
                .all()
            )

            all_steps = Step.objects.filter(project__in=projects).order_by("project_id")
            # Count steps assigned to each worker completed or not
            for worker in workers:
                assigned_steps_count = all_steps.filter(
                    assigned_to=worker.username
                ).count()
                worker.assigned_steps_count = assigned_steps_count
                completed_steps_count = Step.objects.filter(
                    assigned_to=worker.username, is_done=True
                ).count()
                worker.completed_steps_count = completed_steps_count

                if worker.completed_steps_count > 0:
                    worker.progress_percentage = (
                        worker.completed_steps_count / worker.assigned_steps_count
                    ) * 100
                else:
                    worker.progress_percentage = 0
        else:
            return redirect("home")

        context["projects"] = projects
        context["user"] = user
        context["workers"] = workers

        return render(request, "workers.html", context=context)
