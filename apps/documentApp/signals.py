from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ApplicationForm, Statistics, PublishForm, Document
from ..userApp.models import Profile, UserAccount
from django.contrib.auth.models import Group

""" Crea y actualiza estadística  """
@receiver(post_save, sender=ApplicationForm)
def create_or_update_statistics_requests(sender, instance, created, **kwargs):
    
    document = instance.document
    stats, _ = Statistics.objects.get_or_create(document=document)
    if created:
        stats.requests += 1
        stats.save(update_fields=['requests'])

""" Cuando se crea un documento se crea un publish_form """
@receiver(post_save, sender=Document)
def create_publish_form(sender, instance, created, **kwargs):
    if created:
        # Obtén el ID de 'teacher_guide' desde el documento
        teacher_guide_id = instance.teacher_guide

        try:
            # Convierte el ID en una instancia de UserAccount
            teacher_guide_user = UserAccount.objects.get(id=teacher_guide_id)
        except UserAccount.DoesNotExist:
            print(f"UserAccount con ID {teacher_guide_id} no encontrado.")  # Mensaje de error con print
            return

        try:
            # Obtén el Profile asociado al UserAccount
            teacher_guide_profile = Profile.objects.get(user=teacher_guide_user)
        except Profile.DoesNotExist:
            print(f"Profile asociado al UserAccount {teacher_guide_user.email} no encontrado.")  # Mensaje de error con print
            return

        try:
            # Obtén el grupo "Director de Carrera"
            group_director = Group.objects.get(name="Director de Carrera")
        except Group.DoesNotExist:
            print("El grupo 'Director de Carrera' no existe.")  # Mensaje de error con print
            return

        # Verifica si el campo personalizado `group` coincide con "Director de Carrera"
        is_director = teacher_guide_user.group == group_director
        print(f"¿El usuario {teacher_guide_user.email} es Director de Carrera? {is_director}")  # Mensaje informativo

        # Establece el estado inicial según el rol de usuario
        initial_state = '2' if is_director else '1'

        # Crea el PublishForm con el estado inicial adecuado
        PublishForm.objects.create(
            state=initial_state,
            document=instance,
            teacher_guide=teacher_guide_profile
        )
        print(f"PublishForm creado con estado {initial_state} para el documento {instance.id}.")  