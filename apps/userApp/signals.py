from .models import Profile, UserAccount
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver

@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

""" Cifra la contraseña para la creación de usuario en el admin """
@receiver(pre_save, sender=UserAccount)
def hash_password(sender, instance, **kwargs):
    if instance.pk:  # Si el usuario ya existe
        old_password = UserAccount.objects.get(pk=instance.pk).password
        if instance.password != old_password:  # Verifica si la contraseña cambió
            instance.password = make_password(instance.password)
    else:  # Si es un usuario nuevo
        instance.password = make_password(instance.password)