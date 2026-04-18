from django.urls import path
from . import views
from .views import WeeklogListCreateView, ApproveLogView, Workplace_SupervisorLogsView, Academic_SupervisorLogsView,DashboardView,AssignPlacementView

urlpatterns = [
    path('test/',views.test , name='test'),
    path('weekly-log/',WeeklogListCreateView.as_view()),
    path('workplace_supervisor/logs/',Workplace_SupervisorLogsView.as_view()),
    path('academic_supervisor/logs/',Academic_SupervisorLogsView.as_view()),
    path('supervisor/<int:pk>/approve/',ApproveLogView.as_view()),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('api/admin/assign_placement/',AssignPlacementView.as_view())
    ]
