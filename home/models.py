from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_project_manager = models.BooleanField(default=False)
    manager = models.CharField(max_length=255, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        permissions = [
            ("can_create_users", "Can create new users"),
        ]


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    description = models.TextField()
    todays_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Step(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    todays_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    assigned_to = models.CharField(max_length=100)
    file = models.FileField(upload_to="static/steps/", null=True, blank=True)
    sign_sheet = models.FileField(upload_to="static/steps/", null=True, blank=True)

    def __str__(self):
        return self.name
