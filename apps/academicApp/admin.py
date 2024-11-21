from django.contrib import admin
from .models import Section, Signature, Career, Area
from django.apps import AppConfig

# Register your models here.
admin.site.register(Section)
admin.site.register(Signature)
admin.site.register(Career)
admin.site.register(Area)

