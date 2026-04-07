from django.db import models
from django.conf import settings

STATUS_CHOICES=[
    ("draft",'draft'),
    ("submitted",'submitted'),
    ('reviewed','Reviewed'),
    ('approved','Approved'),
]
# Create your models here.


    
# Profile per role

class Student(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    university=models.CharField(max_length=100)
    internship_start_date=models.DateField()
    internship_end_date=models.DateField()

    def __str__(self):
        return f"Student : {self.user.username}"
    
class AcademicSupervisor(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    university=models.CharField(max_length=100)
    faculty=models.CharField(max_length=100)

    def __str__(self):
        return f'Academic Supervisor : {self.user.username}'
    
class WorkplaceSupervisor(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    company=models.CharField(max_length=100)
    department=models.CharField(max_length=100)

    def __str__(self):
        return f'Workplace Supervisor : {self.user.username}'

class Adminstrator(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    office=models.CharField(max_length=100)

    def __str__(self):
        return f"Admin : {self.user.username}"
    
class InternshipPlacement(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    academic_supervisor=models.ForeignKey(AcademicSupervisor,on_delete=models.CASCADE)
    workplace_supervisor=models.ForeignKey(WorkplaceSupervisor,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100)
    company_address=models.CharField(max_length=100)
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
      return f"Week {self.week_number} - {self.placement.student.user.username}"
    

class EvaluationCriteria(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    weight=models.DecimalField(max_digits=5,decimal_places=2)
    
    def __str__(self):
        return self.name
class Evaluation(models.Model):
    placement=models.ForeignKey(InternshipPlacement,on_delete=models.CASCADE)
    criteria=models.ForeignKey(EvaluationCriteria,on_delete=models.CASCADE)
    evaluator=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    score=models.DecimalField(max_digits=3,decimal_places=2)
    comments=models.TextField(blank=True)
    date_evaluated=models.DateField()

    def __str__(self):
        return f'{self.placement} - {self.criteria}'
    