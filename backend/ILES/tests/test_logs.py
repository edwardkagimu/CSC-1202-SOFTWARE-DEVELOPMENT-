import pytest
from ILES.models import Student,WeeklyLog, InternshipPlacement,AcademicSupervisor,WorkplaceSupervisor
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()
@pytest.mark.django_db
def test_create_weekly_log():

    client = APIClient()

    #student = Student.objects.create(user=User.objects.create(username="s1"))
    #wp = WorkplaceSupervisor.objects.create(name="WP")
    #ac = AcademicSupervisor.objects.create(name="AC")
    
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


    placement = InternshipPlacement.objects.create(
        student=student,
        workplace_supervisor=wp,
        academic_supervisor=ac,
        company_name="Tech",
        company_address="Kampala",
        start_date="2026-05-01",
        end_date="2026-08-01"
    )

    client.force_authenticate(user=student.user)

    data = {
        "week_number": 1,
        "placement_id": placement.id,
        "activities":"Storage",
        "challenges":"no",
        "skills_learned":"none"
    }

    response = client.post("/weekly-log/", data)
    print(response.content)

    assert response.status_code in [200, 201] 

@pytest.mark.django_db
def test_weekly_log_without_placement():

    client = APIClient()

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


    client.force_authenticate(user=student.user)

    
    data = {
        "week_number": 1,
     #no placement id
        "activities":"Storage",
        "challenges":"no",
        "skills_learned":"none"
    }

    response = client.post("/weekly-log/", data)

    assert response.status_code == 400

@pytest.mark.django_db
def test_duplicate_weekly_log_blocked():

    client = APIClient()

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

    placement = InternshipPlacement.objects.create(
        student=student,
        workplace_supervisor=wp,
        academic_supervisor=ac,
        company_name="Tech",
        company_address="Kampala",
        start_date="2026-05-01",
        end_date="2026-08-01"
    )

    WeeklyLog.objects.create(
        placement=placement,
        week_number=1,
        activities="Storage",
        challenges="no",
        skills_learned="none",
        date_submitted="2026-05-06"
    )

    client.force_authenticate(user=student.user)

    data = {
        "week_number": 1,
        "placement_id": placement.id,
        "activities":"Storage",
        "challenges":"no",
        "skills_learned":"none"

    }


    response = client.post("/weekly-log/", data)
    print(response.content)
    assert response.status_code in [400, 409]


@pytest.mark.django_db
def test_weekly_log_deadline_passed():

    client = APIClient()
    
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


    placement = InternshipPlacement.objects.create(
        student=student,
        workplace_supervisor=wp,
        academic_supervisor=ac,
        company_name="Tech",
        company_address="Kampala",
        start_date="2020-01-01",  # old date to force deadline fail
        end_date="2020-02-01"
    )

    client.force_authenticate(user=student.user)

    data = {
        "week_number": 10,
        "placement_id": placement.id,
        "activities":"Storage",
        "challenges":"no",
        "skills_learned":"none"
    }

    response = client.post("/weekly-log/", data)

    assert response.status_code == 400
