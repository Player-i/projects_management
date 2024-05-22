from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from home.models import MyUser, MyUserManager, Project, Step
from .serializers import UserSerializer, EmailLoginFormSerializer, UserRegistrationSerializer, ProjectSerializer, StepSerializerSee, StepSerializerChange, IsUserProjectAdminSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import base64
from django.core.files.base import ContentFile
from django.contrib.sessions.models import Session
from rest_framework.parsers import JSONParser


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
                Project.objects.filter(author=user, step__isnull=False)
                .order_by("-id")  # Reverse order by project ID
                .distinct()
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
        steps_serializer = StepSerializerSee(steps, many=True)

        # Combine project and steps data in a dictionary
        project_data = {
            'project': project_serializer.data,
            'steps': steps_serializer.data
        }

        return JsonResponse(project_data)
   
@api_view(['GET'])
def get_step_details(request, step_id):
    step = Step.objects.get(id=step_id)
    print(step.file2)

    if request.method == "GET":
        # Serialize the step data
        step_serializer = StepSerializerSee(step)
        print(step.file2)
        return JsonResponse(step_serializer.data, status=status.HTTP_200_OK)




# @api_view(['POST'])
@csrf_exempt
def edit_step(request, step_id):
    try:
        step = Step.objects.get(id=step_id)
    except Step.DoesNotExist:
        return JsonResponse({'detail': 'Step not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StepSerializerChange(data=data)

        if serializer.is_valid():
            # Update other fields as needed
            description = serializer.validated_data.get('description')
            is_done = serializer.validated_data.get('is_done')
            step.description = description
            step.is_done = is_done

            # Save the Step instance

            # Extract and save File1 URI
            file_uri = serializer.validated_data.get('file')
            if file_uri and not file_uri.startswith("/static"):
                file_content = base64.b64decode(file_uri.split(',')[0])
                step.file.save(f'file_{step_id}.jpg', ContentFile(file_content), save=True)
                print(f"File saved: {step.file.path}")

            # Extract and save File2 URI
            file2_uri = serializer.validated_data.get('file2')
            if file2_uri and not file2_uri.startswith("/static"):
                file2_content = base64.b64decode(file2_uri.split(',')[0])
                step.file2.save(f'file2_{step_id}.jpg', ContentFile(file2_content), save=True)
                print(f"File2 saved: {step.file2.path}")

            # Extract and save File3 URI
            file3_uri = serializer.validated_data.get('file3')
            if file3_uri and not file3_uri.startswith("/static"):
                file3_content = base64.b64decode(file3_uri.split(',')[0])
                step.file3.save(f'file3_{step_id}.jpg', ContentFile(file3_content), save=True)
                print(f"File3 saved: {step.file3.path}")

            # Extract and save File4 URI
            file4_uri = serializer.validated_data.get('file4')
            if file4_uri and not file4_uri.startswith("/static"):
                file4_content = base64.b64decode(file4_uri.split(',')[0])
                step.file4.save(f'file4_{step_id}.jpg', ContentFile(file4_content), save=True)
                print(f"File4 saved: {step.file4.path}")

            # Extract and save Sign Sheet URI
            sign_sheet_uri = serializer.validated_data.get('sign_sheet')
            if sign_sheet_uri and not sign_sheet_uri.startswith("/static"):
                sign_sheet_content = base64.b64decode(sign_sheet_uri.split(',')[0])
                step.sign_sheet.save(f'sign_sheet_{step_id}.jpg', ContentFile(sign_sheet_content), save=True)
                print(f"Sign Sheet saved: {step.sign_sheet.path}")

            
            step.save() 


            return JsonResponse({'message': 'Step updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
@csrf_exempt
def update_project_from_smartsheet(request):
    if request.method == 'POST':
        # Extract the rows_data from the POST request
        rows_data = JSONParser().parse(request)
        # Process the received data
        rows_data = rows_data['rows_data']        
        for row_data in rows_data:
            # Perform any necessary actions with the row data
            # For example, you could create or update objects in your database
            
            # Example: Print the row data
            primary = row_data.get('Primary')
            status = row_data.get('Status')
            date = row_data.get('Date')
            customer = row_data.get('Customer')
            contact = row_data.get('Contact')
            contact_phone = row_data.get('Contact Phone')
            address = row_data.get('Address')
            scope = row_data.get('Scope')
            number = row_data.get('#')
            on_site_time = row_data.get('On Site Time')
            employee_one = row_data.get('Employee One')
            employee_two = row_data.get('Employee Two')
            employee_three = row_data.get('Employee Three')
            employee_four = row_data.get('Employee Four')
            work_to_be_performed = row_data.get('Work to be Performed')
            shop_arrival_time = row_data.get('Shop Arrival Time')
            vehicle = row_data.get('Vehicle')
            equipment_needed = row_data.get('Equipment Needed')
            special_instruction = row_data.get('Special Instruction')

            project_name = f'{customer}, {address} {contact_phone}'
            user = MyUser.objects.get(email="spalko@budgetmaintenance.com")
            project, created = Project.objects.get_or_create(name=project_name, defaults={'author': user})
            project.equipment = equipment_needed
            project.vehicle = vehicle
            project.todays_date = date
            project.description = work_to_be_performed
            project.save()

            steps_created = False
            employees = [employee_one, employee_two, employee_three, employee_four]
            for employee in employees:
                try:
                    user = MyUser.objects.get(email=employee)
                    if user is not None:
                        # Create a step for the employee
                        step = Step.objects.create(project=project, assigned_to=user.username)
                        step.description = special_instruction
                        step.todays_date = date
                        step.name = ""
                        step.save()
                        steps_created = True
                except MyUser.DoesNotExist:
                    pass

            # Check if steps are created, if not, delete the project
            if not steps_created:
                project.delete()





        # Respond with a success message or any other relevant data
        return JsonResponse({'message': 'Data received successfully'})
    else:
        # Handle GET requests or any other unsupported methods
        return JsonResponse({'error': 'Unsupported method'}, status=405)

@api_view(['GET'])
def logout_view(request, email):
    print(email)
    if request.method == "GET":
        user = MyUser.objects.get(email=email)
        print(user)
        request.session['user_id'] = user.id
        print(request)

        logout(request)

        return JsonResponse({'detail': 'Logout successful'})

@api_view(['GET'])
def is_user_project_manager(request, email):
    if request.method == "GET":
        user = MyUser.objects.get(email=email)
        is_project_admin = user.is_project_manager
        # Return a single boolean value without using many=True
        return JsonResponse({'is_project_manager': is_project_admin})


