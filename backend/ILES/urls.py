from django.urls import path
from . import views
from .views import WeeklogListCreateView, ApproveLogView,EvaluationCriteriaListView,EvaluationView,SubmitLogView,DeleteLogView,UsersListView, Workplace_SupervisorLogsView, Academic_SupervisorLogsView,DashboardView,AssignPlacementView

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
    path('evaluation/create/', EvaluationView.as_view()),
    path('evaluation/criteria/', EvaluationCriteriaListView.as_view()),
    ]
