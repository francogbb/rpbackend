from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ApplicationForm, Statistics, PublishForm, Document
from ..userApp.models import Profile
from django.shortcuts import get_object_or_404

@receiver(post_save, sender=ApplicationForm)
def create_or_update_statistics_requests(sender, instance, created, **kwargs):
    
    document = instance.document
    stats, _ = Statistics.objects.get_or_create(document=document)
    if created:
        stats.requests += 1
        stats.save(update_fields=['requests'])
        

@receiver(post_save, sender=ApplicationForm)
def create_or_update_statistics_views(sender, instance, created, **kwargs):
    document = instance.document
    stats, _ = Statistics.objects.get_or_create(document=document)
    if created and instance.state == '2':
        stats.views += 1
        stats.save(update_fields=['views'])
        
@receiver(post_save, sender=Document)
def create_publish_form(sender, instance, created, **kwargs):
    if created:
        teacher_guide_id = instance.teacher_guide  # Suponiendo que esto es un string
        teacher_guide_instance = get_object_or_404(Profile, id=teacher_guide_id)
        PublishForm.objects.create(
            state='1',  # Estado 'Pendiente' como valor inicial
            document=instance,
            teacher_guide=teacher_guide_instance  # Ahora es una instancia de Profile
        ) 