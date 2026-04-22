from django.contrib import admin
from .models import WeeklyLog,InternshipPlacement,Student,WorkplaceSupervisor,AcademicSupervisor

# Register your models here.

@admin.register(WeeklyLog)
class  WeeklyLogAdmin(admin.ModelAdmin):
    list_display=("week_number","placement","status","date_submitted")
    list_filter=("status",)
    search_fields=("placement__student__user__username",)

admin.site.register(InternshipPlacement)
admin.site.register(Student)
admin.site.register(AcademicSupervisor)
admin.site.register(WorkplaceSupervisor)