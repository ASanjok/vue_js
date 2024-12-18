from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import FlightSerializerGetAll
from .models import PositionData


class FlightsGetAllAPIView(APIView):
    def get(self, request):
        flights = PositionData.objects.select_related('place').all()
        serializer = FlightSerializerGetAll(flights, many=True)
        return Response(serializer.data)