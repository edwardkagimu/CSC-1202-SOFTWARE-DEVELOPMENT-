from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.models import CustomUser
from django.contrib.auth import authenticate
# Create your views here.

@api_view(['POST'])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')

    if not username or not password:
        return Response({'error':'username and password required'})
    
    user = authenticate(request,username=username,password=password)
    if user is None:
        return Response({'error':'Invalid crendentials'})
    else:
        return Response({'message':'login successfully'})


@api_view(['POST'])
def signup(request):
    username=request.data.get('username')
    email=request.data.get('email')
    password=request.data.get('password')
    role=request.data.get('role')

    if not username or not email or not password or not role:
        return Response({'error':'All feilds required'},status=400)
    
    #create user with hashed password
    user=CustomUser.objects.create_user(username=username,email=email,password=password,role=role)

    return Response({'message':'signup successfully'},status=201)

@api_view(['GET'])
def test_token(request):
    return Response({'okay'})