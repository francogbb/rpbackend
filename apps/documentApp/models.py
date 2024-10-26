from django.db import models
from ..userApp.models import Profile, CustomGroup
from ..academicApp.models import Area
from datetime import datetime

# Create your models here.

class TypeDocument(models.Model):

    TYPE_CHOICES = [
            ('1', 'Proyecto de Integración'),
            ('2', 'Seminario de Título'),
            ('3', 'Seminario de Grado'),
            ('4', 'Proyecto de Título'),
        ]

    type_name = models.CharField(max_length=50, choices=TYPE_CHOICES)


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
    abstract = models.CharField(max_length=300)
    type_access = models.BooleanField(default=False) # True = Público, False = Privado
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    academic_degree = models.CharField(max_length=55, choices=DEGREE_CHOICES)
    qualification = models.IntegerField()
    document = models.FileField(upload_to='filePDF/')# Cree el campo de document para que se guarde dentro de la carpeta filePDF
    publisher = models.CharField(max_length=55, choices=PUBLISHER_CHOICES) # Datos duros: Universidad Inacap, Intituto Profesional Inacap, Centro de formacion tecnico Inacap
    identifier = models.CharField(max_length=255) # Identificador URL de documento
    teacher_guide = models.CharField(max_length=100) # No tiene relación debido a la subida de documentos antiguos
    entry_date = models.DateTimeField(auto_now_add=True)
    available_date = models.DateTimeField(auto_now_add=True) 
    publication_year = models.IntegerField(default=datetime.now().year)
    author = models.ManyToManyField(CustomGroup)
    type_document = models.ForeignKey(TypeDocument, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title


class Statistics(models.Model):
    views = models.IntegerField(default=0)
    requests = models.IntegerField(default=0)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Estadísticas de {self.document.title}"
    

class ApplicationForm(models.Model):
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()  # Fecha de expiración ------------------------------ Cambiar settings (CL)
    document = models.ForeignKey(Document , on_delete=models.CASCADE)  # Relación con Document
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Relación con Profile
   
    def __str__(self):
        return f"Formulario de Solicitud hecho por {self.student.first_name} para el documento: {self.document.title}"
    

class Record(models.Model):
    application = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE)  # Relación con Application_Form
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Relación con Profile

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