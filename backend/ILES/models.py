from django.db import models
from django.conf import settings
from datetime import timedelta
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
    reg_no = models.CharField(max_length=50, unique=True) 
    university=models.CharField(max_length=100)
    internship_start_date = models.DateField(null=True, blank=True)
    internship_end_date = models.DateField(null=True, blank=True)
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
    student=models.OneToOneField(Student,on_delete=models.CASCADE)
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
    activities=models.CharField(max_length=100)
    challenges=models.CharField(max_length=100)
    skills_learned=models.CharField(max_length=100)
    date_submitted=models.DateField(max_length=100)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='draft')
    deadline=models.DateField(null=True,blank=True)
    #Enforce deadline 

    
    def __str__(self):
      return f"Week {self.week_number} - {self.placement.student.user.username}"

class WorkplaceEvaluation(models.Model):
    placement = models.OneToOneField(InternshipPlacement,on_delete=models.CASCADE)

    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    punctuality = models.IntegerField()
    teamwork = models.IntegerField()
    communication = models.IntegerField()
    smartness = models.IntegerField()
    discipline = models.IntegerField()

    comments = models.TextField(blank=True)

    workplace_total = models.DecimalField(max_digits=5,decimal_places=2,default=0)

    date_evaluated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Workplace Evaluation - {self.placement}"
    
class AcademicEvaluation(models.Model):
    placement = models.OneToOneField(InternshipPlacement,on_delete=models.CASCADE)

    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    technical_skills = models.IntegerField()
    report_quality = models.IntegerField()
    problem_solving = models.IntegerField()
    presentation = models.IntegerField()

    comments = models.TextField(blank=True)

    academic_total = models.DecimalField(max_digits=5,decimal_places=2,default=0)

    date_evaluated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Academic Evaluation - {self.placement}"