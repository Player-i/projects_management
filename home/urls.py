"""
URL configuration for events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("home/", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("create/", views.create_project, name="create_project"),
    path("workers/", views.workers, name="workers"),
    path("create_users/", views.create_users, name="create_users"),
    path("step/<int:step_id>/", views.step_details, name="step_details"),
    path("project/<int:project_id>/", views.project_details, name="project_details"),
    path("edit/<int:project_id>/", views.edit_project, name="edit_project"),
    path("edit_step/<int:step_id>/", views.edit_step, name="edit_step"),
    path(
        "delete_project/<int:project_id>/", views.delete_project, name="delete_project"
    ),
    path(
        "duplicate/<int:project_id>/", views.duplicate_project, name="duplicate_project"
    ),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),

]
