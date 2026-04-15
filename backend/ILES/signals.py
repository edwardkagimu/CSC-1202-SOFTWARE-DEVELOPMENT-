#for automatic creation of my users profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Student, WorkplaceSupervisor, AcademicSupervisor,Adminstrator

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:

        if instance.role == "student":
            Student.objects.create(
                user=instance,

            )

        elif instance.role == "workplace_supervisor":
            WorkplaceSupervisor.objects.create(user=instance)

        elif instance.role == "academic_supervisor":
            AcademicSupervisor.objects.create(user=instance)
        elif instance.role == "admin":
            Adminstrator.objects.create(user=instance)