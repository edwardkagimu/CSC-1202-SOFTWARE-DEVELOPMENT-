from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import WeeklyLog,Evaluation,Student,WorkplaceSupervisor,AcademicSupervisor,InternshipPlacement
from rest_framework.response import Response
from .serializers import WeeklyLogSerializer,StudentSerializer,WorkplaceSupervisorSerializer,AcademicSupervisorSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from datetime import date
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
             "draft":WeeklyLog.objects.filter(placement__student=student,status="draft").count(),
             "reviewed":WeeklyLog.objects.filter(placement__student=student,status="reviewed").count(),
             "approved_logs":WeeklyLog.objects.filter(placement__student=student,status="approved").count(),
             "evaluations":Evaluation.objects.filter(placement__student=student).count(),
            }
         elif user.role == 'workplace_supervisor':
             workplace_supervisor=user.workplacesupervisor
             data={
                 "pending_logs":WeeklyLog.objects.filter(placement__workplace_supervisor=workplace_supervisor,status="submitted").count(),
                 "reviewed_logs":WeeklyLog.objects.filter(placement__workplace_supervisor=workplace_supervisor,status="reviewed").count(),
             }
         elif user.role == 'academic_supervisor':
              academic_supervisor=user.academicsupervisor
              data={
                 "pending_logs":WeeklyLog.objects.filter(placement__academic_supervisor=academic_supervisor,status="reviewed").count(),
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
         return Response({
             "user":{
                 "username":user.username,
                 "role":role,
                 "reg_no": user.student.reg_no if role == "student" else None
             },
             "data":data
         })
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
        
        #to validate week_number
        week = request.data.get("week_number")
        if WeeklyLog.objects.filter(placement=placement, week_number=week).exists():
               return Response({"error": "Log for this week already exists"}, status=400)
        
        serializer=WeeklyLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(placement=placement,status="draft",date_submitted=date.today())
            return Response (serializer.data)
        return Response(serializer.errors,status=400)

class Workplace_SupervisorLogsView(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request):
        if request.user.role != "workplace_supervisor":
            return Response ({"error":"Only Workplace supervisors can access"},status=403)
        try:
          logs=WeeklyLog.objects.filter(placement__workplace_supervisor=request.user.workplacesupervisor,status="submitted")
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
          logs=WeeklyLog.objects.filter(placement__academic_supervisor=request.user.academicsupervisor,status="reviewed")
          serializer=WeeklyLogSerializer(logs,many=True)
          return Response(serializer.data)
        except Exception as e:
            return Response ({'error':str(e)})  

class ApproveLogView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,pk):
        if request.user.role not in ["academic_supervisor", "workplace_supervisor", "admin"]:
             return Response({"error": "Not allowed"}, status=403)
        try:
            log=WeeklyLog.objects.get(id=pk)
           
        except WeeklyLog.DoesNotExist:
            return Response ({"error" : "Log not Found"})
            
        user=request.user
        if user.role == "workplace_supervisor":
            if log.placement.workplace_supervisor != user.workplacesupervisor:
                return Response({"error": "Not your log"}, status=403)
            
            if log.status != "submitted":
                return Response({"error": "Only submitted logs can be reviewed"}, status=400)
            log.status = "reviewed"
        elif user.role == "academic_supervisor":
            if log.placement.academic_supervisor != user.academicsupervisor:
                return Response({"error": "Not your log"}, status=403)
            
            if log.status != "reviewed":
                return Response({"error": "Only submitted logs can be reviewed"}, status=400)

            log.status = "approved"
        else:
            return Response({"error": "Not allowed"}, status=403)
        
        #update field
        log.save()
        serializer=WeeklyLogSerializer(log)
        return Response({"message": f"Log {log.status}"})

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
        

class SubmitLogView(APIView):
    permission_classes = [IsAuthenticated,IsStudent]

    def patch(self, request, pk):
        try:
            log = WeeklyLog.objects.get(id=pk,placement__student=request.user.student)
        except WeeklyLog.DoesNotExist:
            return Response({"error": "Log not found"}, status=404)

        if log.status != "draft":
            return Response({"error": "Only draft logs can be submitted"}, status=400)
        log.status = "submitted"
        log.save()

        return Response({"message": "Log submitted successfully"})
    
class UsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        workplaces = WorkplaceSupervisor.objects.all()
        academics = AcademicSupervisor.objects.all()

        return Response({
            "students": StudentSerializer(students, many=True).data,
            "workplace_supervisors": WorkplaceSupervisorSerializer(workplaces, many=True).data,
            "academic_supervisors": AcademicSupervisorSerializer(academics, many=True).data,
        })
    
class DeleteLogView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def delete(self, request, pk):
        try:
            log = WeeklyLog.objects.get(id=pk,placement__student=request.user.student)
        except WeeklyLog.DoesNotExist:
            return Response({"error": "Log not found"}, status=404)

        # only delete logs still in draft and submitted
        if log.status in ['approved', 'reviewed'] :
            return Response(
                {"error": "Only draft and submitted logs can be deleted"},status=400 )

        log.delete()
        return Response({"message": "Log deleted successfully"})