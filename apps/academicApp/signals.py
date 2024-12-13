from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Section
from django.contrib.auth.models import Group

""" Cambia el rol de profesor a profesor guía cuando se asigna un profesor a una sección """
@receiver(post_save, sender=Section)
def update_teacher_group(sender, instance, created, **kwargs):
    if created:
        teacher_guide = instance.teacher_guide

        if teacher_guide:
            try:
                # Busca el grupo "Profesor Guía" por nombre
                group_profesor_guia = Group.objects.get(name="Profesor Guía")
            except Group.DoesNotExist:
                print("El grupo 'Profesor Guía' no existe")
                return

            # Actualiza el grupo si no coincide
            if teacher_guide.group != group_profesor_guia:
                teacher_guide.group = group_profesor_guia
                teacher_guide.save()
                print(f"Grupo actualizado para el usuario {teacher_guide.email}")
