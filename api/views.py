from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from home.models import MyUser, MyUserManager, Project, Step
from .serializers import UserSerializer, EmailLoginFormSerializer, UserRegistrationSerializer, ProjectSerializer, StepSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import base64
from django.core.files.base import ContentFile



# Create your views here.

# Get all the users (to test api)
@api_view([ "GET"])
def user_list(request):

    if request.method == "GET":
        user_list = MyUser.objects.all()
        serializer = UserSerializer(user_list, many=True)
        return JsonResponse(serializer.data, safe=False)



# API Login
@csrf_exempt
@api_view(['POST'])
def email_login(request):
    if request.method == 'POST':
        serializer = EmailLoginFormSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Create an authentication form
            auth_form = authenticate(request, email=username, password=password)

            if auth_form is not None:
                # Log in the user
                login(request, auth_form)
                print("Login work")
                return JsonResponse({'detail': 'Login successful'}, status=200)
                
            else:
                return JsonResponse({'detail': 'Invalid credentials'}, status=401)
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)

    return JsonResponse({'detail': 'Method not allowed'}, status=405)


# API Register
@csrf_exempt
@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
    
        if serializer.is_valid():
            name = serializer.validated_data['username']
            password = serializer.validated_data['password1']
            email = serializer.validated_data['email']
            print("User")
            print(name)
            print(email)
            print(password)
            
            # MyUserManager.create_user(username=name, email=email, password=password)
            MyUser.objects.create_user(username= name, email = email, password = password, is_project_manager=True)
            auth_form = authenticate(request, email=email, password=password)
            
            if auth_form is not None:
                login(request, auth_form)
                return JsonResponse({'detail': 'Registration and login successful'}, status=201)
            else:
                return JsonResponse({'detail': 'Error during login after registration'}, status=401)
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)

    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@api_view(['GET'])
def get_user_projects(request, email):
    if request.method == "GET":
        user = MyUser.objects.get(email=email)
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
                Project.objects.filter(
                    step__assigned_to=user.username,  # Filter projects based on steps assigned to the user
                    step__project__author=manager,  # Additionally, the project's author must be the user's manager
                )
                .distinct()
                .prefetch_related("step_set")
                .order_by("-id")
            )

        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_project_details(request, project_id, email):
   user = MyUser.objects.get(email=email)
   print(user)
   if request.method == "GET":
        project = get_object_or_404(Project, id=project_id)
        
        # Assuming you have a serializer for your Step model
        if user.is_project_manager:
            steps = project.step_set.all()
        else:
            # If the user is not the manager, filter steps based on assigned_to
            steps = project.step_set.filter(assigned_to=user.username)

        # Serialize the project and steps
        project_serializer = ProjectSerializer(project)
        steps_serializer = StepSerializer(steps, many=True)

        # Combine project and steps data in a dictionary
        project_data = {
            'project': project_serializer.data,
            'steps': steps_serializer.data
        }

        return JsonResponse(project_data)
   

@csrf_exempt
@api_view(['POST'])
def edit_step(request, step_id):
    
    step = Step.objects.get(id=step_id)

    if request.method == 'POST':
        # Extract and save File1 URI
        file_uri = request.data.get('file')
        if file_uri:
            file_content = base64.b64decode(file_uri.split(',')[1])
            step.file.save(f'file_{step_id}.jpg', ContentFile(file_content), save=True)
            print(f"File saved: {step.file.path}")

        # Extract and save File2 URI
        file2_uri = request.data.get('file2')
        if file2_uri:
            file2_content = base64.b64decode(file2_uri.split(',')[1])
            step.file2.save(f'file2_{step_id}.jpg', ContentFile(file2_content), save=True)
            print(f"File2 saved: {step.file2.path}")

        # Extract and save File3 URI
        file3_uri = request.data.get('file3')
        if file3_uri:
            file3_content = base64.b64decode(file3_uri.split(',')[1])
            step.file3.save(f'file3_{step_id}.jpg', ContentFile(file3_content), save=True)
            print(f"File3 saved: {step.file3.path}")

        # Extract and save File4 URI
        file4_uri = request.data.get('file4')
        if file4_uri:
            file4_content = base64.b64decode(file4_uri.split(',')[1])
            step.file4.save(f'file4_{step_id}.jpg', ContentFile(file4_content), save=True)
            print(f"File4 saved: {step.file4.path}")

        # Extract and save Sign Sheet URI
        sign_sheet_uri = request.data.get('sign_sheet')
        if sign_sheet_uri:
            sign_sheet_content = base64.b64decode(sign_sheet_uri.split(',')[1])
            step.sign_sheet.save(f'sign_sheet_{step_id}.jpg', ContentFile(sign_sheet_content), save=True)
            print(f"Sign Sheet saved: {step.sign_sheet.path}")

        # Update description and is_done
        description = request.data['description']
        is_done = request.data['is_done']

        step.description = description
        step.is_done = is_done.capitalize()
        step.save()

        print("Step updated successfully")

        return JsonResponse({'message': 'Step updated successfully.'}, status=status.HTTP_200_OK)

