from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# Main user model
class CustomUser(AbstractUser):
    # Django choices require a list of tuples each having two values
    # (value_stored_in_database, human_readable_value)
    Roles_Choices=[
        ('student','Student Intern'),
        ('work_supervior', 'Workplace Supervisor' ),
        ('academic_supervisor','Academic Supervisor'),
        ('admin','Administrator'),
    ]
    role=models.CharField(max_length=20,choices=Roles_Choices)

    def __str__(self):
        return f'{self.username} : {self.role}'