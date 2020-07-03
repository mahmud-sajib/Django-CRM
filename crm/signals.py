from django.contrib.auth.models import Group
from .models import Customer
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create profile signal
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            group = Group.objects.get(name='admin')
            instance.groups.add(group)
            
        else:
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            Customer.objects.create(user=instance, name=instance.username,)
            print("Profile Created")

