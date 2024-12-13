from .models import Profile, UserAccount
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver

""" Crea el profile de un usuario al momento de ser registrado """
@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

""" Cifra la contraseña para la creación de usuario en el admin """
@receiver(pre_save, sender=UserAccount)
def hash_password(sender, instance, **kwargs):
    # Solo cifra si la contraseña no está ya cifrada
    if not instance.password.startswith("pbkdf2_sha256$"):
        instance.password = make_password(instance.password)
