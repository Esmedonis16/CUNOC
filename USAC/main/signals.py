from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import docentes

@receiver(post_save, sender=docentes)
def add_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Docentes')
        instance.user.groups.add(group)
        instance.save()
