from django.db import models
from ..userApp.models import Profile, CustomGroup
from ..academicApp.models import Area
from datetime import datetime
from cryptography.fernet import Fernet
from django.core.files.base import ContentFile

class TypeDocument(models.Model):

    type_name = models.CharField(max_length=50) # Proyecto de Título, Seminario de Título....
    def __str__(self):
        return self.type_name


class Document(models.Model):
    PUBLISHER_CHOICES = [
        ('1', 'Universidad Inacap'),
        ('2', 'Instituto Profesional Inacap'),
        ('3', 'Centro de Formación Técnica Inacap'),
    ]
    
    DEGREE_CHOICES = [
        ('1', 'Técnico de Nivel Superior'),
        ('2', 'Ingeniero'),
        ('3', 'Licenciado'),
    ]
    
    title = models.CharField(max_length=100)
    abstract = models.CharField()
    type_access = models.BooleanField(default=False) # True = Público, False = Privado
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    academic_degree = models.CharField(max_length=55, choices=DEGREE_CHOICES)# Datos duros: Técnico de Nivel Superior, Ingeniero y Licenciado
    qualification = models.IntegerField()
    document = models.FileField(upload_to='filePDF/')
    publisher = models.CharField(max_length=55, choices=PUBLISHER_CHOICES) # Datos duros: Universidad Inacap, Intituto Profesional Inacap, Centro de formacion tecnico Inacap
    identifier = models.CharField(max_length=255) # URL del perfil del documento
    teacher_guide = models.CharField(max_length=100, null=True, blank=True) # Se debe cambiar a Uploader. Este campo hace referencia al usuario que suba un documento académico
    entry_date = models.DateTimeField(auto_now_add=True)
    available_date = models.DateTimeField(auto_now_add=True) 
    publication_year = models.IntegerField(default=datetime.now().year)
    author = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    type_document = models.ForeignKey(TypeDocument, on_delete=models.CASCADE) 
    encryption_key = models.BinaryField(null=True, blank=True) # Guardar la llave de encriptación
    career = models.ForeignKey('academicApp.Career', on_delete=models.CASCADE, null=True, blank=True)
    signature = models.ForeignKey('academicApp.Signature', on_delete=models.CASCADE, null=True, blank=True)
    teacher_name = models.CharField(max_length=100, null=True, blank=True) # Nombre del Profesor Guía del Documento
    def __str__(self):
        return self.title


class Statistics(models.Model):
    views = models.IntegerField(default=0)
    requests = models.IntegerField(default=0)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    last_viewed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Estadísticas de {self.document.title}"
    

class ApplicationForm(models.Model):
    
    STATE_FORM = [
        ('1', 'Pendiente'),
        ('2', 'Aprobado'),
        ('3', 'Rechazado'),
    ]
    state = models.CharField(choices=STATE_FORM, max_length=1, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True) 
    document = models.ForeignKey(Document , on_delete=models.CASCADE)  
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)  
    def __str__(self):
        return f"Formulario de Solicitud hecho por {self.student.first_name} para el documento: {self.document.title}"
    
""" Pendiente eliminación de modelo """
class Record(models.Model):
    application = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE)  
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  

    def __str__(self):
        return f"Historial de {self.user.first_name}"


class PublishForm(models.Model):
    
    STATE_CHOICES = [
        ('1', 'Pendiente'),
        ('2', 'Aprobado'),
        ('3', 'Rechazado'),
    ]
    state = models.CharField(max_length=1, choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    teacher_guide = models.ForeignKey(Profile, on_delete=models.CASCADE)