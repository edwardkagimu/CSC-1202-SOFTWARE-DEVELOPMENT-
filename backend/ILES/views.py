from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import WeeklyLog,WorkplaceEvaluation,AcademicEvaluation,Student,WorkplaceSupervisor,AcademicSupervisor,InternshipPlacement
from rest_framework.response import Response
from .serializers import WeeklyLogSerializer,AcademicEvaluationSerializer,WorkplaceEvaluationSerializer,StudentSerializer,WorkplaceSupervisorSerializer,AcademicSupervisorSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from datetime import date, timedelta
from accounts.models import CustomUser
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
          if not hasattr(user, "student"):
             return Response({"error": "Student profile missing"}, status=400)
          student=user.student
          placement = InternshipPlacement.objects.filter(student=student).first()

          workplace_score = 0
          academic_score = 0
          final_score = 0

          if placement:
              workplace_eval = WorkplaceEvaluation.objects.filter(placement=placement).first()
              academic_eval = AcademicEvaluation.objects.filter(placement=placement).first()
          
              if workplace_eval:
                    workplace_score = float(workplace_eval.workplace_total)

              if academic_eval:
                  academic_score = float(academic_eval.academic_total)

              final_score = (workplace_score + academic_score)
          data={
             "logs": WeeklyLog.objects.filter(placement__student=student).count(),
             "draft":WeeklyLog.objects.filter(placement__student=student,status="draft").count(),
             "reviewed":WeeklyLog.objects.filter(placement__student=student,status="reviewed").count(),
             "approved_logs":WeeklyLog.objects.filter(placement__student=student,status="approved").count(),
             "workplace_score":workplace_score,
             "academic_score":academic_score,
             "final_score":round(final_score,2),
            }
          
         elif user.role == 'workplace_supervisor':
             workplace_supervisor=user.workplacesupervisor
             data={
                 "pending_logs":WeeklyLog.objects.filter(placement__workplace_supervisor=workplace_supervisor,status="submitted").count(),
                 "reviewed_logs":WeeklyLog.objects.filter(placement__workplace_supervisor=workplace_supervisor,status="reviewed").count(),
                 "evaluated_students":WorkplaceEvaluation.objects.filter(evaluator=user).count()
             }
         elif user.role == 'academic_supervisor':
              academic_supervisor=user.academicsupervisor
              data={
                 "pending_logs":WeeklyLog.objects.filter(placement__academic_supervisor=academic_supervisor,status="reviewed").count(),
                 "approved_logs":WeeklyLog.objects.filter(placement__academic_supervisor=academic_supervisor,status="approved").count(),
                 "evaluated_students":AcademicEvaluation.objects.filter(evaluator=user).count()
             }
         elif role == 'admin' or user.is_staff:
             
             data={
                 "students":Student.objects.count(),
                 "total_logs":WeeklyLog.objects.count(),
                 "approved_logs":WeeklyLog.objects.filter(status="approved").count(),
                 "submitted_logs":WeeklyLog.objects.filter(status="submitted").count(),
                 "reviewed_logs":WeeklyLog.objects.filter(status="reviewed").count(),
                 "workplace_evaluations":WorkplaceEvaluation.objects.count(),
                 "academic_evaluations":AcademicEvaluation.objects.count()
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
        
        # DEADLINE LOGIC
        week =int(request.data.get("week_number"))
        # assume each week starts from placement.start_date
        week_start = placement.start_date + timedelta(days=(week - 1) * 7)
        deadline = week_start + timedelta(days=7)  # end of week

        if date.today() > deadline:
            return Response({"error": "Submission deadline passed"}, status=400)

        
        #to validate week_number prevent duplicates
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

class WorkplaceEvaluationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, placement_id):

        if request.user.role != "workplace_supervisor":
            return Response({"error": "Not allowed"}, status=403)
        try:
         placement = InternshipPlacement.objects.get(id=placement_id)
        except InternshipPlacement.DoesNotExist:
            return Response({"error": "Placement not found"},status=404)
        serializer = WorkplaceEvaluationSerializer(data=request.data)

        if serializer.is_valid():

            punctuality = int(request.data["punctuality"])
            teamwork = int(request.data["teamwork"])
            communication = int(request.data["communication"])
            smartness = int(request.data["smartness"])
            discipline = int(request.data["discipline"])

            workplace_total = ( punctuality * 0.10 + teamwork * 0.10 + communication* 0.05 + smartness * 0.05 + discipline * 0.10) 

            serializer.save( placement=placement,evaluator=request.user, workplace_total=workplace_total)

            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=400)
    
#for fetching backend comment
class WorkplaceEvaluationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, placement_id):
        try:
            evaluation = WorkplaceEvaluation.objects.get( placement_id=placement_id )
            serializer = WorkplaceEvaluationSerializer(evaluation)
            return Response(serializer.data)
        except WorkplaceEvaluation.DoesNotExist:
            return Response({"error": "No workplace evaluation found"},status=404)
        
class AcademicEvaluationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, placement_id):
        if request.user.role != "academic_supervisor":return Response({"error": "Not allowed"},status=403)

        placement = InternshipPlacement.objects.get(id=placement_id)

        technical = int(request.data["technical_skills"])
        report = int(request.data["report_quality"])
        solving = int(request.data["problem_solving"])
        presentation = int(request.data["presentation"])

        academic_total = (technical * 0.10  + report * 0.20 + solving * 0.20 + presentation * 0.10)

        serializer = AcademicEvaluationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(placement=placement,evaluator=request.user,academic_total=academic_total)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class PlacementScoreView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, placement_id):
        try:
            placement = InternshipPlacement.objects.get(id=placement_id)
            workplace = WorkplaceEvaluation.objects.filter(placement=placement).first()
            academic = AcademicEvaluation.objects.filter(placement=placement).first()
            workplace_score = (workplace.workplace_total if workplace else 0)
            academic_score = (academic.academic_total if academic else 0)
            final_score = (workplace_score + academic_score)

            return Response({
                "placement": placement.id,
                "workplace_score": workplace_score,
                "academic_score": academic_score,
                "final_score": round(final_score, 2)})
        except Exception as e:
            return Response({"error": str(e)})

class AssignedStudentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        role = request.user.role
        if role == "workplace_supervisor":
            supervisor = request.user.workplacesupervisor
            placements = InternshipPlacement.objects.filter(workplace_supervisor=supervisor)

        elif role == "academic_supervisor":
            supervisor = request.user.academicsupervisor
            placements = InternshipPlacement.objects.filter(academic_supervisor=supervisor)

        else:
            return Response({"error": "Not allowed"},status=403)

        data = [
            {
                "placement_id": p.id,
                "student_id": p.student.id,
                "username": p.student.user.username,
                "reg_no": p.student.reg_no
            }
            for p in placements
        ]

        return Response(data)

class ManageUsersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        role=(request.user.role or "").strip().lower()
        user=request.user
        if role !=  "admin" or user.is_staff:
            return Response({"error": "Not allowed"},status=403 )

        students = Student.objects.all()

        data = []

        for s in students:
            placement = InternshipPlacement.objects.filter( student=s).first()
            data.append({
                "id": s.user.id,
                "username": s.user.username,
                "role": "student",
                "reg_no": s.reg_no,
                "workplace_supervisor":placement.workplace_supervisor.user.username
                    if placement and placement.workplace_supervisor
                    else None,

                "academic_supervisor":
                    placement.academic_supervisor.user.username
                    if placement and placement.academic_supervisor
                    else None
            })

        workplace_supervisors = WorkplaceSupervisor.objects.all()

        for w in workplace_supervisors:
            data.append({
                "id": w.user.id,
                "username": w.user.username,
                "role": "workplace_supervisor"
            })

        academic_supervisors = AcademicSupervisor.objects.all()
        for a in academic_supervisors:
            data.append({
                "id": a.user.id,
                "username": a.user.username,
                "role": "academic_supervisor"
            })

        return Response(data)
    
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, user_id):
        if request.user.role != "admin":
            return Response({"error": "Not allowed"},status=403)

        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted"})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)