from django.urls import path
from . import views
from .views import WeeklogListCreateView,ManageUsersView,DeleteUserView, ApproveLogView,AssignedStudentsView,AcademicEvaluationView,WorkplaceEvaluationView,WorkplaceEvaluationDetailView,PlacementScoreView,SubmitLogView,DeleteLogView,UsersListView, Workplace_SupervisorLogsView, Academic_SupervisorLogsView,DashboardView,AssignPlacementView

urlpatterns = [
    path('test/',views.test , name='test'),
    path('weekly-log/',WeeklogListCreateView.as_view()),
    path('submit-log/<int:pk>/',SubmitLogView.as_view(),name='submit'),
    path('workplace_supervisor/logs/',Workplace_SupervisorLogsView.as_view()),
    path('delete-log/<int:pk>/', DeleteLogView.as_view()),
    path('academic_supervisor/logs/',Academic_SupervisorLogsView.as_view()),
    path('supervisor/<int:pk>/approve/',ApproveLogView.as_view()),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('api/users/',UsersListView.as_view(),name='users'),
    path('api/admin/assign_placement/',AssignPlacementView.as_view()),

    path('evaluation/score/<int:placement_id>/', PlacementScoreView.as_view()),
    path('workplace-comment/<int:placement_id>/',WorkplaceEvaluationDetailView.as_view()),
    path('academic-evaluation/<int:placement_id>/',AcademicEvaluationView.as_view()),
    path('workplace-evaluation/<int:placement_id>/',WorkplaceEvaluationView.as_view()),
    path("assigned-students/",AssignedStudentsView.as_view()),

    path("manage-users/", ManageUsersView.as_view()),
    path("api/delete-user/<int:user_id>/",DeleteUserView.as_view()),
    ]

