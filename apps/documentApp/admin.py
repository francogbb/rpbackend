from django.contrib import admin
from .models import Document, Statistics, ApplicationForm, PublishForm, Record, TypeDocument
# Register your models here.

admin.site.register(TypeDocument)
admin.site.register(Document)
admin.site.register(Statistics)
admin.site.register(ApplicationForm)
admin.site.register(PublishForm)
admin.site.register(Record)