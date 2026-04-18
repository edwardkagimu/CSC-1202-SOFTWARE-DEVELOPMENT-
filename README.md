# CSC 1202: SOFTWARE DEVELOPMENT 
Project for group 2
Group members
1. Chandiga Siraji            25/U/26195/EVE         2500726195
2. Kagimu Edward           25/U/03386/EVE         2500703386
3. Ssewajje Elvin Alex       25/U/03589/EVE         2500703589
4. Mary Micheal Eliaba   25/X/03444                  2500703444

# Internship Logging & Evaluation System API

Base URL:
http://127.0.0.1:8000/

# 1. Authentication

## User Signup
POST /accounts/signup/

Request:
{
  "username"
  "password"
  "email"
  "role"
}

Response:
{
  "message": "User created successfully"
}

## Login
POST /accounts/login/

Request:
{
  "username": "alex",
  "password": "1234"
}

Response:
{
  "access": "jwt_token",
  "refresh": "jwt_refresh_token"
}
# 2. Dashboard

GET /dashboard/

Headers:
Authorization: Bearer <access_token> 

Response (Student):
{
  "total_logs": 5,
  "approved_logs": 3
}

Response (Supervisor):
{
  "pending_logs": 10
}

# 3. Weekly Logs

## Create Weekly Log
POST weekly-logs/
placement
week_number
activities
challenges
skills_learned
date_submitted
status

Headers:
Authorization: Bearer <token>

Request:
{
  "title": "Week 1 report",
  "content": "Worked on backend APIs"
}

## Get Logs
GET weekly-logs/

## Assgn Placements by Admin
POST api/admin/assign_placement/
  #required fields
    "student_id"
    "workplace_supervisor_id"
    "academic_supervisor_id"
    "company_name"
    "company_address"
    "start_date"
    "end_date"

