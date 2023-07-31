from django.contrib import admin
from .models import MyUser, Project, Step

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Project)
admin.site.register(Step)
