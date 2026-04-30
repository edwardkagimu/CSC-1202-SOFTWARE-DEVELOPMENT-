from rest_framework import serializers
from .models import  Student, AcademicSupervisor, WorkplaceSupervisor, WeeklyLog, Evaluation, EvaluationCriteria, InternshipPlacement, Adminstrator
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','role']

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
     
    class Meta:
        model=Student
        fields=['id','username','student_reg_no']

class WorkplaceSupervisorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model=WorkplaceSupervisor
        fields=['id','username']

class WeeklyLogSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='placement.student.user.username',read_only=True)
    student_reg_no = serializers.CharField(source='placement.student.reg_no',read_only=True)
    placement_id = serializers.IntegerField(source='placement.id',read_only=True)
    class Meta:
        model=WeeklyLog
        fields=['id','placement_id','student_reg_no','student_username','week_number','activities','challenges','skills_learned','date_submitted','status']
        read_only_fields=['status','placement','date_submitted',]

class AdminstratorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Adminstrator
        fields='__all__'

class AcademicSupervisorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model=AcademicSupervisor
        fields=['id','username']

class InternshipPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model=InternshipPlacement
        fields='__all__'

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=EvaluationCriteria
        fields='__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Evaluation
        fields='__all__'