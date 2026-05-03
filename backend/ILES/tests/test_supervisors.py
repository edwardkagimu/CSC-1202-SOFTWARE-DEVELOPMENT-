import pytest
from ILES.models import Student,WeeklyLog, InternshipPlacement,AcademicSupervisor,WorkplaceSupervisor
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User=get_user_model()

@pytest.mark.django_db
def test_workplace_can_review_log():

    client = APIClient()

     # Create workplace supervisor
    workplace_supervisor = User.objects.create_user(
        username="worksuper1",
        email="work@test.com",
        password="pass123",
    )
    workplace_supervisor.role = "workplace_supervisor"
    workplace_supervisor.save()
    wp=WorkplaceSupervisor.objects.create(
        user=workplace_supervisor,
        company="Bidco",
        department="ICT",
    )

    student_user = User.objects.create_user(
        username="student1",
        email="student@test.com",
        password="pass123"
    )
    student_user.role = "student"
    student_user.save()

    student = Student.objects.create(
        user=student_user,
        reg_no="CS2025/001"
    )

    academic_supervisor = User.objects.create_user(
        username="acdsuper1",
        email="acd@test.com",
        password="pass123"
    )
    academic_supervisor.role = "academic_supervisor"
    academic_supervisor.save()
    ac=AcademicSupervisor.objects.create(
        user=academic_supervisor,
        faculty="acad1",
        university="acadtest.com",
    )

    placement = InternshipPlacement.objects.create(
        student=student,
        workplace_supervisor=wp,
        academic_supervisor=ac,
        company_name="Tech",
        company_address="Kampala",
        start_date="2026-05-01",
        end_date="2026-08-01"
    )


    log = WeeklyLog.objects.create(
        week_number=1,
        placement=placement,
        activities="Storage",
        challenges="no",
        skills_learned="none",
        status="submitted",
        date_submitted="2026-05-06"
    )


    client.force_authenticate(user=wp.user)

    data = {
        "status": "reviewed"
    }

    response = client.patch(f"/supervisor/{log.id}/approve/", data)

    assert response.status_code == 200

@pytest.mark.django_db
def test_academic_can_approve_reviewed_log():

    client = APIClient()

    workplace_supervisor = User.objects.create_user(
        username="worksuper1",
        email="work@test.com",
        password="pass123",
    )
    workplace_supervisor.role = "workplace_supervisor"
    workplace_supervisor.save()
    wp=WorkplaceSupervisor.objects.create(
        user=workplace_supervisor,
        company="Bidco",
        department="ICT",
    )

    student_user = User.objects.create_user(
        username="student1",
        email="student@test.com",
        password="pass123"
    )
    student_user.role = "student"
    student_user.save()

    student = Student.objects.create(
        user=student_user,
        reg_no="CS2025/001"
    )

    academic_supervisor = User.objects.create_user(
        username="acdsuper1",
        email="acd@test.com",
        password="pass123"
    )
    academic_supervisor.role = "academic_supervisor"
    academic_supervisor.save()
    ac=AcademicSupervisor.objects.create(
        user=academic_supervisor,
        faculty="acad1",
        university="acadtest.com",
    )

    placement = InternshipPlacement.objects.create(
        student=student,
        workplace_supervisor=wp,
        academic_supervisor=ac,
        company_name="Tech",
        company_address="Kampala",
        start_date="2026-05-01",
        end_date="2026-08-01"
    )


    log = WeeklyLog.objects.create(
        week_number=1,
        placement=placement,
        activities="Storage",
        challenges="no",
        skills_learned="none",
        date_submitted="2026-05-06",
        status="reviewed"

    )

    client.force_authenticate(user=ac.user)

    data = {
        "status": "approved"
    }

    response = client.patch(f"/supervisor/{log.id}/approve/", data)

    assert response.status_code == 200
