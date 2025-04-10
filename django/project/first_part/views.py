# views.py
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PositionData
from .serializers import PositionDataSerializer

from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer

from rest_framework.exceptions import NotFound
from django.utils.timezone import now
from datetime import timedelta
from .serializers import PreviousePositionsSerializer

from rest_framework.permissions import IsAuthenticated

class PlaneDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, callsign):
        try:
            # Найти последнюю запись по `call_sign`
            latest_plane = PositionData.objects.filter(call_sign=callsign).order_by('-id').first()
            
            if not latest_plane:
                return Response({"error": "plane is not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Сериализовать данные
            serializer = PositionDataSerializer(latest_plane)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterSerializer(ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class PreviousePositionsView(APIView):
    def get(self, request, call_sign):
        """
        Получить позиции самолета по call_sign за последние 5 минут.
        """
        current_time = now()
        positions = PositionData.objects.filter(
            call_sign=call_sign,
            position__isnull=False,  # Исключаем записи без координат
            # time_received__gte=current_time - timedelta(minutes=5)  # Записи за последние 5 минут
        )# .order_by('-time_received')

        if not positions.exists():
            raise NotFound({"detail": f"Позиции для {call_sign} не найдены за последние 5 минут."})

        serializer = PreviousePositionsSerializer(positions, many=True)
        return Response({"call_sign": call_sign, "positions": serializer.data})
    permission_classes = [AllowAny]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User

class AccountInfoView(APIView):
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)

    def put(self, request):
        """Обновление данных пользователя"""
        user = request.user
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.email = request.data.get("email", user.email)
        user.save()
        return Response(
            {"message": "Данные обновлены успешно."},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        """Удаление аккаунта пользователя"""
        user = request.user
        user.delete()
        return Response(
            {"message": "Аккаунт успешно удалён."},
            status=status.HTTP_204_NO_CONTENT,
        )
