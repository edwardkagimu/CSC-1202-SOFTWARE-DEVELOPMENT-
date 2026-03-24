from django.db import models
from django.contrib.auth.models import AbstractUser

STATUS_CHOICES=[
    ("draft",'draft'),
    ("submitted",'submitted'),
    ('reviewed','Reviewed'),
    ('approved','Approved'),
]
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
    
# Profile per role

class Student(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    university=models.CharField(max_length=100)
    internship_start_date=models.DateField()
    internship_end_date=models.DateField()

    def __str__(self):
        return f"Student : {self.user.username}"
    
class AcademicSupervisor(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    university=models.CharField(max_length=100)
    faculty=models.CharField(max_length=100)

    def __str__(self):
        return f'Academic Supervisor : {self.user.username}'
    
class WorkplaceSupervisor(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    company=models.CharField(max_length=100)
    department=models.CharField(max_length=100)

    def __str__(self):
        return f'Workplace Supervisor : {self.user.username}'

class Adminstrator(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    office=models.CharField(max_length=100)

    def __str__(self):
        return f"Admin : {self.user.username}"
    
class InternshipPlacement(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    academic_supervisor=models.ForeignKey(AcademicSupervisor,on_delete=models.CASCADE)
    workplace_supervisor=models.ForeignKey(WorkplaceSupervisor,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100)
    comapany_address=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()

    def __str__(self):
        return f'{self.student.user.username}  Internship'
    
class WeeklyLog(models.Model):
    placement=models.ForeignKey(InternshipPlacement,on_delete=models.CASCADE)
    week_number=models.IntegerField()
    activities=models.CharField()
    challenges=models.CharField()
    skills_learned=models.CharField()
    date_submitted=models.DateField()
    status=models.CharField(choices=STATUS_CHOICES,default='draft')
    def __str__(self):
        return 
    

class EvaluationCriteria(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    weight=models.DecimalField(max_digits=5,decimal_places=2)
    
    def __str__(self):
        return self.name
class Evaluation(models.Model):
    placement=models.ForeignKey(InternshipPlacement,on_delete=models.CASCADE)
    criteria=models.ForeignKey(EvaluationCriteria,on_delete=models.CASCADE)
    evaluator=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    score=models.DecimalField(max_digits=3,decimal_places=2)
    comments=models.TextField(blank=True)
    date_evaluated=models.DateField()

    def __str__(self):
        return f'{self.placement} - {self.criteria}'
    