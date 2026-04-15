from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import WeeklyLog,Evaluation,Student
from rest_framework.response import Response
from .serializers import WeeklyLogSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def test (request):
    return (HttpResponse("Working..."))

class DashboardView(APIView):
    permission_classes=[IsAuthenticated]
    def  get(self,request):
        
        try:
         user = request.user
         if user.role == 'student':
          student=user.student
          data={
             "logs": WeeklyLog.objects.filter(placement__student=student).count(),
             "approved_logs":WeeklyLog.objects.filter(placement__student=student,status="approved").count(),
             "evaluations":Evaluation.objects.filter(placement__student=student).count(),
            }
         elif user.role == 'workplace_supervisor':
             workplace_supervisor=user.workplacesupervisor
             data={
                 "pending_logs":WeeklyLog.objects.filter(placement__workplace_supervisor=workplace_supervisor).count(),
             }
         elif user.role == 'academic_supervisor':
              academic_supervisor=user.academicsupervisor
              data={
                 "pending_logs":WeeklyLog.objects.filter(placement__academic_supervisor=academic_supervisor).count(),
             }
         elif user.role == 'admin':
             admin=user.is_staff
             data={
                 "students":Student.objects.count(),
                 "logs":WeeklyLog.objects.count(),
                 "evaluations":Evaluation.objects.count()
             } 
         return Response(data)
        except Exception as e:
            return Response({"error":str(e)})
class WeeklogListCreateView(APIView):
    permission_classes=[IsAuthenticated]
 
    def get(self,request):
        print("USER:",request.user)
        if not request.user.is_authenticated:
 
            return Response(str(request.user),status=401)
        
        try:
         logs=WeeklyLog.objects.filter(placement__student=request.user.student)
         serializer=WeeklyLogSerializer(logs,many =True)
         return Response (serializer.data)
        except Exception as e:
            return Response ({'error':str(e)})
    
    def post(self,request):
        serializer=WeeklyLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response (serializer.data)
        return Response(serializer.errors)

class Workplace_SupervisorLogsView(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request):
        try:
          logs=WeeklyLog.objects.filter(placement__workplace_supervisor=request.user.workplace_supervisor)
          serializer=WeeklyLogSerializer(logs,many=True)
          return Response(serializer.data)
        except Exception as e:
            return Response ({'error':str(e)})  

class Academic_SupervisorLogsView(APIView):
    def get (self,request):
        try:
          logs=WeeklyLog.objects.filter(placement__academic_supervisor=request.user.academic_supervisor)
          serializer=WeeklyLogSerializer(logs,many=True)
          return Response(serializer.data)
        except Exception as e:
            return Response ({'error':str(e)})  

class ApproveLogView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,pk):
        try:
            log=WeeklyLog.objects.get(id=pk)
           
        except WeeklyLog.DoesNotExist:
            return Response ({"error" : "Log not Found"})
            
        #update field
        log.approved=True
        log.status="approved"
        log.save(update_fields=["status"])
        serializer=WeeklyLogSerializer(log,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors)

