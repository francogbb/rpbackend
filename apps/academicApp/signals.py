from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Section
from userApp.models import UserAccount
from django.contrib.auth.models import Group

@receiver(post_save, sender=Section)
def update_teacher_group(sender, instance, created, **kwargs):
    if created:
        # Obtener el teacher_guide relacionado
        teacher_guide = instance.teacher_guide

        # Verificar el grupo actual del teacher_guide
        if teacher_guide.group is None or teacher_guide.group.id != 2:
            # Obtener el grupo con id 2
            try:
                group_2 = Group.objects.get(id=2)
            except Group.DoesNotExist:
                print("El grupo con id 2 no existe")
                return

            # Actualizar el grupo del teacher_guide
            teacher_guide.group = group_2
            teacher_guide.save()
