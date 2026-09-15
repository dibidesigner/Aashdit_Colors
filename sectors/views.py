from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Sector
from .serializers import PopularSectorSerializer,SectorCreateSerializer,SectorSerializer,SampleUISerializer


class PopularSectorListView(APIView):

    def get(self, request):

        sectors = (
            Sector.objects
            .filter(is_active=True)
            .prefetch_related(
                "characteristics",
                "sample_uis",
            )
            .select_related(
                "color_palette"
            )
        )

        serializer = PopularSectorSerializer(
            sectors,
            many=True
        )

        return Response(
            {
                "success": True,
                "count": sectors.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
            serializer = SectorCreateSerializer(
                data=request.data
            )

            if serializer.is_valid():

                sector = serializer.save()

                return Response(
                    {
                        "success": True,
                        "message": "Sector created successfully.",
                        "data": SectorSerializer(
                            sector
                        ).data
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
