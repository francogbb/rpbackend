from django.db import models
from django.contrib.auth.models import User
from ..academicApp.models import Section

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=10)
    role = models.CharField(max_length=10)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email}" 

class CustomGroup(models.Model):
    group_name = models.CharField(max_length=100)
    teacher_guide = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name

class GroupUser(models.Model):
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    student = models.CharField(max_length=200)

    def __str__(self):
        return self.group.group_name