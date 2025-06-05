# views.py

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PositionData
from .serializers import PositionDataSerializer, PreviousePositionsSerializer

from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import NotFound
from django.utils.timezone import now
from datetime import timedelta

# Skats lai iegūtu jaunāko informāciju par lidmašīnu pēc tās call_sign
class PlaneDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, callsign):
        try:
            latest_plane = PositionData.objects.filter(call_sign=callsign).order_by('-id').first()

            if not latest_plane:
                return Response({"error": "Lidmašīna nav atrasta"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PositionDataSerializer(latest_plane)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Serializators lietotāja reģistrācijai
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

# Skats reģistrācijai
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Skats, lai iegūtu iepriekšējās pozīcijas pēdējo 5 minūšu laikā
class PreviousePositionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, call_sign):
        """
        Iegūst lidmašīnas pozīcijas pēc call_sign pēdējo 5 minūšu laikā.
        """
        current_time = now()
        positions = PositionData.objects.filter(
            call_sign=call_sign,
            position__isnull=False,
            time_received__gte=current_time - timedelta(minutes=5)
        ).order_by('-time_received')

        if not positions.exists():
            raise NotFound({"detail": f"Nav atrastas pozīcijas priekš {call_sign} pēdējo 5 minūšu laikā."})

        serializer = PreviousePositionsSerializer(positions, many=True)
        return Response({"call_sign": call_sign, "positions": serializer.data})

# Skats informācijas iegūšanai/parādīšanai, lietotāja datu atjaunošanai un dzēšanai
class AccountInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Atgriež pašreizējā lietotāja informāciju
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)

    def put(self, request):
        # Atjauno pašreizējā lietotāja informāciju
        user = request.user
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.email = request.data.get("email", user.email)
        user.save()
        return Response(
            {"message": "Dati veiksmīgi atjaunināti."},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        # Dzēš pašreizējo lietotāja kontu
        user = request.user
        user.delete()
        return Response(
            {"message": "Konts veiksmīgi dzēsts."},
            status=status.HTTP_204_NO_CONTENT,
        )
