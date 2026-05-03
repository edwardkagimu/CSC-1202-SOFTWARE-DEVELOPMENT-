
import pytest
from django.contrib.auth import get_user_model
from ILES.models import Student, InternshipPlacement,AcademicSupervisor,WorkplaceSupervisor
from rest_framework.test import APIClient
from django.contrib.auth.models import User
User = get_user_model()
client=APIClient()
@pytest.mark.django_db
def test_create_placement():

    admin=User.objects.create_user(
        username="admin",
        password="admin",
        is_staff=True
    )
    client.force_authenticate(user=admin)

    # Create student user
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

    defaults={
        "student_id":student.id,
        "workplace_supervisor_id":wp.id,
        "academic_supervisor_id":ac.id,
        "company_name":"tech",
        "company_address":"kawempe",
        "start_date":"2026-05-01",
        "end_date":"2026-08-01"
    }
    
    url="/api/admin/assign_placement/"

    response=client.post(url,defaults,format="json")
    print(response.data)
    print(InternshipPlacement.objects.count())
    assert response.status_code in [200,201]
    assert InternshipPlacement.objects.count()==1


@pytest.mark.django_db
def test_prevent_duplicate_placement():

    client = APIClient()

    admin=User.objects.create_user(
     username="admin",
     password="admin",
     is_staff=True
    )
    client.force_authenticate(user=admin)

    # Create student user
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

    # First placement
    InternshipPlacement.objects.create(
        student=student,

        workplace_supervisor=wp,
        academic_supervisor=ac,
        company_name="Tech Corp",
        company_address="Kampala",
        start_date="2026-06-08",
        end_date="2026-08-10"
    )

    data = {
        "student_id": student.id,
        "workplace_supervisor_id": wp.id,
        "academic_supervisor_id": ac.id,
        "company_name": "Another Company",
        "company_address": "Kampala",
        "start_date":"2026-05-01",
        "end_date":"2026-08-03"
    }
    
    url="/api/admin/assign_placement/"

    response = client.post(url, data, format="json")

    # Should reject duplicate
    assert response.status_code in [400, 

409]
