from django.urls import path
from .views import RegisterUserView, UserInfoView, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('user/<int:user_id>/', UserInfoView.as_view(), name='user-info'),
]