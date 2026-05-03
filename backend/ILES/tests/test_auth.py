import pytest 
from django.contrib.auth import get_user_model
from ILES.models import Student

User = get_user_model()

@pytest.mark.django_db
def test_create_student_user():
    user = User.objects.create_user(
        username="student1",
        email="student1@test.com",
        password="testpass123",
    )
    user.role = "student"
    user.save()

    student = Student.objects.create(
        user=user,
        reg_no="CS2025/001"
    )

    assert student.user.username == "student1"
    assert student.reg_no == "CS2025/001"

@pytest.mark.django_db
def test_create_workplace_supervisor():
    user = User.objects.create_user(
        username="supervisor1",
        email="sup@test.com",
        password="pass123"
    )
    user.role = "workplace_supervisor"
    user.save()

    assert user.role == "workplace_supervisor"

@pytest.mark.django_db
def test_create_academic_supervisor():
    user = User.objects.create_user(
        username="academic1",
        email="acad@test.com",
        password="pass123"
    )
    user.role = "academic_supervisor"
    user.save()

    assert user.role == "academic_supervisor"