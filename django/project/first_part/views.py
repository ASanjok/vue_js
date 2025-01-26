# views.py
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import PositionData
from .serializers import PositionDataSerializer

class PlaneDetailView(APIView):
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

