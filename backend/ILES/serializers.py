from rest_framework import serializers
from .models import  Student, AcademicSupervisor, WorkplaceSupervisor, WeeklyLog, Evaluation, EvaluationCriteria, InternshipPlacement, Adminstrator
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','role']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'

class WorkplaceSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkplaceSupervisor
        fields='__all__'

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
    class Meta:
        model=AcademicSupervisor
        fields='__all__'

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