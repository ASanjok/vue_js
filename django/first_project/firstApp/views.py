from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from .serializers import AnimeSerializerGetAll, AnimeSerializerPostNameEpisode
# from .models import Anime

from .serializers import FlightSerializerGetAll
from .models import PositionData


# class FirstProjectAPIView(APIView):
#     def get(self, request):
#         Animes = Anime.objects.select_related('statusF').all()
#         serializer = AnimeSerializerGetAll(Animes, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = AnimeSerializerPostNameEpisode(data=request.data)

        
#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlightsGetAllAPIView(APIView):
    def get(self, request):
        flights = PositionData.objects.select_related('place').all()
        serializer = FlightSerializerGetAll(flights, many=True)
        return Response(serializer.data)