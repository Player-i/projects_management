from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),
    path('email-login/', views.email_login, name='email-login'),
    path('user-registration/', views.user_registration, name='user-registration'),
    path('get-user-projects/<str:email>/', views.get_user_projects, name='get_user_projects'),
    path('project-details/<int:project_id>/<str:email>/', views.get_project_details, name='get_project_details'),
    path('edit-step/<int:step_id>/', views.edit_step, name='edit-step'),
    path('logout/<str:email>/', views.logout_view, name='logout'),
    path('get_step_details/<int:step_id>/', views.get_step_details, name='get-step-details')

] 