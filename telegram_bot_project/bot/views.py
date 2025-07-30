from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TelegramUser
from .serializers import TelegramUserSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

class RegisterUserView(APIView):
    def post(self, request):
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            if TelegramUser.objects.filter(user_id=user_id).exists():
                user = TelegramUser.objects.get(user_id=user_id)
                return Response(TelegramUserSerializer(user).data)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(TelegramUser, user_id=user_id)
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)

def home_view(request):
    return HttpResponse("""
        <h1>Добро пожаловать в API Telegram бота!</h1>
        <p>Доступные эндпоинты:</p>
        <ul>
            <li><a href="/api/register/">/api/register/</a> - POST для регистрации пользователя</li>
            <li><a href="/api/user/1/">/api/user/&lt;user_id&gt;/</a> - GET для получения информации о пользователе</li>
            <li><a href="/admin/">/admin/</a> - Админ-панель</li>
        </ul>
    """)