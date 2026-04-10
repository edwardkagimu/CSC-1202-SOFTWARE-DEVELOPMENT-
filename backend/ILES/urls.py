from django.urls import path
from . import views
from .views import WeeklogListCreateView, ApproveLogView, Workplace_SupervisorLogsView, Academic_SupervisorLogsView

urlpatterns = [
    path('test/',views.test , name='test'),
    path('weekly-log/',WeeklogListCreateView.as_view()),
    path('workplace_supervisor/logs/',Workplace_SupervisorLogsView.as_view()),
    path('academic_supervisor/logs',Academic_SupervisorLogsView.as_view()),
    path('supervisor/approve/',ApproveLogView.as_view())
    ]
