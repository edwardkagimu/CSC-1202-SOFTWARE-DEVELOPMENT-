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
        fields=['id','username']

class WorkplaceSupervisorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model=WorkplaceSupervisor
        fields=['id','username']

class WeeklyLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=WeeklyLog
        fields='__all__'
        read_only_fields=['status']

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