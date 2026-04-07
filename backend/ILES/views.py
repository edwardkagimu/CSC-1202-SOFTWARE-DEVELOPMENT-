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
        logs=WeeklyLog.objects.filter(student=request.user)
        serializer=WeeklyLogSerializer(logs,many =True)
        return Response (serializer.data)
    
    def post(self,request):
        serializer=WeeklyLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response (serializer.data)
        return Response(serializer.errors)

class SupervisorLogsView(APIView):
    def get (self,request,supervisor_id):
        logs=WeeklyLog.objects.filter(student__supervisor_id=supervisor_id)
        serializer=WeeklyLogSerializer(logs,many=True)
        return Response(serializer.data)
    
class ApproveLogView(APIView):
    def put(self,request,log_id):
        try:
            log=WeeklyLog.objects.get(id=log_id)
        except WeeklyLog.DoesNotExist:
            return Response ({"error" : "Log not Found"})
        
        log.approved=True
        log.save()
        return Response({"message" : " Log approved"})

