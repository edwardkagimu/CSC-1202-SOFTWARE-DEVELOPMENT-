from django.urls import path,include
from .views import login,signup,test_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('signup/',signup,name='signup'),
    path('test_token/',test_token)
]