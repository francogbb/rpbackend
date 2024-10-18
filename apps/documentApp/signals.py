from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ApplicationForm, Statistics

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