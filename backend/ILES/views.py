from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import WeeklyLog
from rest_framework.response import Response
from .serializers import WeeklyLogSerializer

# Create your views here.

def test (request):
    return (HttpResponse("Working..."))
 
class WeeklogListCreateView(APIView):
    def get(self,request):
        try:
         logs=WeeklyLog.objects.filter(placement__student=request.user)
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
    def get (self,request):
        try:
          logs=WeeklyLog.objects.filter(placement__workplace_supervisor=request.data)
          serializer=WeeklyLogSerializer(logs,many=True)
          return Response({'serializer.data'})
        except Exception as e:
            return Response ({'error':str(e)})  

class Academic_SupervisorLogsView(APIView):
    def get (self,request):
        try:
          logs=WeeklyLog.objects.filter(placement__academic_supervisor=request.data)
          serializer=WeeklyLogSerializer(logs,many=True)
          return Response({'serializer.data'})
        except Exception as e:
            return Response ({'error':str(e)})  

class ApproveLogView(APIView):
    def put(self,request,pk):
        try:
            log=WeeklyLog.objects.get(id=pk)
           
        except WeeklyLog.DoesNotExist:
            return Response ({"error" : "Log not Found"})
            
        #update field
        log.approved=True
        log.save(update_fields=["status","approved"])
        serializer=WeeklyLogSerializer(log,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors)

