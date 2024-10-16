from django.contrib import admin
from .models import Profile, CustomGroup, GroupUser

# Register your models here.

admin.site.register(Profile)
admin.site.register(CustomGroup)
admin.site.register(GroupUser)