from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Partner

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_partner_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'partner':
        Partner.objects.create(user=instance, company_name=instance.username)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_partner_profile(sender, instance, **kwargs):
    if hasattr(instance, 'partner'):
        instance.partner.save()