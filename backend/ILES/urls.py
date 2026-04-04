from django.urls import path
from . import views
from .views import WeeklogListCreateView, ApproveLogView, SupervisorLogsView

urlpatterns = [
    path('test/',views.test , name='test'),
    path('weekly-log/',WeeklogListCreateView.as_view()),
    path('supervisor/logs/',SupervisorLogsView.as_view()),
    path('supervisor/approve/',ApproveLogView.as_view())
    ]
