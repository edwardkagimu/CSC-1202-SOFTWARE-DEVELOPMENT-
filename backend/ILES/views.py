from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import WeeklyLog,Evaluation,Student,WorkplaceSupervisor,AcademicSupervisor,InternshipPlacement
from rest_framework.response import Response
from .serializers import WeeklyLogSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
# Create your views here.

def test (request):
    return (HttpResponse("Working..."))

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_staff or request.user.role == "admin")
        )
    
class DashboardView(APIView):
    permission_classes=[IsAuthenticated]
    def  get(self,request):
        
        try:
         user = request.user
         role = (user.role or "").strip().lower()

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
                 "pending_logs":WeeklyLog.objects.filter(placement__workplace_supervisor=workplace_supervisor,status="submitted").count(),
                 "approved_logs":WeeklyLog.objects.filter(placement__workplace_supervisor=workplace_supervisor,status="approved").count(),
             }
         elif user.role == 'academic_supervisor':
              academic_supervisor=user.academicsupervisor
              data={
                 "pending_logs":WeeklyLog.objects.filter(placement__academic_supervisor=academic_supervisor,status="submitted").count(),
                 "approved_logs":WeeklyLog.objects.filter(placement__academic_supervisor=academic_supervisor,status="approved").count(),
             }
         elif role == 'admin' or user.is_staff:
             
             data={
                 "students":Student.objects.count(),
                 "total_logs":WeeklyLog.objects.count(),
                 "approved_logs":WeeklyLog.objects.filter(status="approved").count(),
                 "pending_logs":WeeklyLog.objects.filter(status="submitted").count(),
                 "evaluations":Evaluation.objects.count()
             } 
         return Response(data)
        except Exception as e:
            return Response({"error":str(e)})
class WeeklogListCreateView(APIView):
    permission_classes=[IsAuthenticated, IsStudent]
 
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
        try:
          placement = InternshipPlacement.objects.get(student=request.user.student)
        except InternshipPlacement.DoesNotExist:
            return Response({"error":"No Placement assigned yet"},status=400)
        serializer=WeeklyLogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(placement=placement)
            return Response (serializer.data)
        return Response(serializer.errors)

class Workplace_SupervisorLogsView(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request):
        if request.user.role != "workplace_supervisor":
            return Response ({"error":"Only Workplace supervisors can access"},status=403)
        try:
          logs=WeeklyLog.objects.filter(placement__workplace_supervisor=request.user.workplacesupervisor)
          serializer=WeeklyLogSerializer(logs,many=True)
          return Response(serializer.data)
        except Exception as e:
            return Response ({'error':str(e)})  

class Academic_SupervisorLogsView(APIView):
    permission_classes=[IsAuthenticated]    
    def get (self,request):
        if request.user.role != "academic_supervisor":
            return Response ({"error":"Only Academic supervisors can access"},status=403)
        try:
          logs=WeeklyLog.objects.filter(placement__academic_supervisor=request.user.academicsupervisor)
          serializer=WeeklyLogSerializer(logs,many=True)
          return Response(serializer.data)
        except Exception as e:
            return Response ({'error':str(e)})  

class ApproveLogView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,pk):
        if request.user.role not in ["academic_supervisor", "workplace_supervisor", "admin"]:
             return Response({"error": "Not allowed"}, status=403)
        try:
            log=WeeklyLog.objects.get(id=pk)
           
        except WeeklyLog.DoesNotExist:
            return Response ({"error" : "Log not Found"})
            
        #update field
        log.approved=True
        log.status="approved"
        log.save(update_fields=["status"])
        serializer=WeeklyLogSerializer(log)
        return Response(serializer.data,status=200)

class AssignPlacementView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def post(self, request):
        try:
         student = Student.objects.get(id=request.data["student_id"])
         wp = WorkplaceSupervisor.objects.get(id=request.data["workplace_supervisor_id"])
         ac = AcademicSupervisor.objects.get(id=request.data["academic_supervisor_id"])

         placement, created = InternshipPlacement.objects.update_or_create(
             student=student,
            #to prevent a student from being assigned multiple times
             defaults={
              "workplace_supervisor":wp,
              "academic_supervisor":ac,
              "company_name":request.data["company_name"],
              "company_address":request.data["company_address"],
              "start_date":request.data["start_date"],
              "end_date":request.data["end_date"]
             }
         )

         return Response({"message": "Assigned successfully",
                           "id": placement.id})
        except Exception as e:
          return Response({"error":str(e)},status=400)