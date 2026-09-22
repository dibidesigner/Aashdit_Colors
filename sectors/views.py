from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ColorPalete

from .models import Sector
from .serializers import (
    PopularSectorSerializer,
    SectorCreateSerializer,
    SectorSerializer,
)


@method_decorator(csrf_exempt, name="dispatch")
class SectorSaveView(APIView):
    """
    API view to handle saving (create/update), fetching, and deleting sector data
    sent from React (e.g. via Axios POST request).
    Exempted from CSRF cookie checks for REST API requests.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, pk=None):
        try:
            sector_id = pk or request.query_params.get("id") or request.query_params.get("sector_id")
            if sector_id:
                try:
                    sector = Sector.objects.prefetch_related(
                        "characteristics",
                        "personality_profiles",
                        "imagery_guidelines",
                        "sample_uis",
                        "component_guidelines",
                        "accessibility_guidelines",
                    ).select_related(
                        "color_palette",
                        "layout_guideline",
                        "typography_guideline",
                        "shape_guideline",
                    ).get(id=sector_id)

                    return Response(
                        {
                            "success": True,
                            "data": SectorSerializer(sector).data
                        },
                        status=status.HTTP_200_OK
                    )
                except Sector.DoesNotExist:
                    return Response(
                        {
                            "success": False,
                            "message": f"Sector with ID {sector_id} not found."
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            sectors = Sector.objects.filter(is_active=True).prefetch_related(
                "characteristics",
                "personality_profiles",
                "imagery_guidelines",
                "sample_uis",
                "component_guidelines",
                "accessibility_guidelines",
            ).select_related(
                "color_palette",
                "layout_guideline",
                "typography_guideline",
                "shape_guideline",
            )

            return Response(
                {
                    "success": True,
                    "count": sectors.count(),
                    "data": SectorSerializer(sectors, many=True).data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, pk=None):
        """
        POST endpoint to save sector data from React (using Axios).
        Saves main sector info along with all nested characteristics, personality profiles,
        color palette, imagery guidelines, layout/typography/shape guidelines, components, sample UI & accessibility.
        """
        try:
            data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
            sector_id = pk or data.get("id") or data.get("sector_id")

            sector_instance = None
            if sector_id:
                sector_instance = Sector.objects.filter(id=sector_id).first()
                if not sector_instance and pk:
                    return Response(
                        {
                            "success": False,
                            "message": f"Sector with ID {pk} not found."
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
                elif not sector_instance:
                    # ID passed in payload does not exist in DB (e.g., client-side temporary ID), remove it to create a new sector
                    data.pop("id", None)
                    data.pop("sector_id", None)

            if sector_instance:
                serializer = SectorCreateSerializer(
                    sector_instance,
                    data=data,
                    partial=True
                )
            else:
                serializer = SectorCreateSerializer(
                    data=data
                )

            if serializer.is_valid():
                sector = serializer.save()

                full_sector = Sector.objects.prefetch_related(
                    "characteristics",
                    "personality_profiles",
                    "imagery_guidelines",
                    "sample_uis",
                    "component_guidelines",
                    "accessibility_guidelines",
                ).select_related(
                    "color_palette",
                    "layout_guideline",
                    "typography_guideline",
                    "shape_guideline",
                ).get(id=sector.id)

                return Response(
                    {
                        "success": True,
                        "message": "Sector updated successfully." if sector_instance else "Sector created successfully.",
                        "data": SectorSerializer(full_sector).data
                    },
                    status=status.HTTP_200_OK if sector_instance else status.HTTP_201_CREATED
                )

            return Response(
                {
                    "success": False,
                    "message": "Validation error",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """
        PUT endpoint for explicit updates
        """
        return self.post(request, pk=pk)

    def delete(self, request, pk=None):
        """
        DELETE endpoint to delete a sector by ID
        """
        try:
            data = request.data if isinstance(request.data, dict) else {}
            sector_id = pk or data.get("id") or data.get("sector_id") or request.query_params.get("id")

            if not sector_id:
                return Response(
                    {
                        "success": False,
                        "message": "Sector ID is required for deletion."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                sector = Sector.objects.get(id=sector_id)
            except Sector.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": f"Sector with ID {sector_id} not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            sector.delete()

            return Response(
                {
                    "success": True,
                    "message": "Sector deleted successfully."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(csrf_exempt, name="dispatch")
class PopularSectorListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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

            full_sector = Sector.objects.prefetch_related(
                "characteristics",
                "personality_profiles",
                "imagery_guidelines",
                "sample_uis",
                "component_guidelines",
                "accessibility_guidelines",
            ).select_related(
                "color_palette",
                "layout_guideline",
                "typography_guideline",
                "shape_guideline",
            ).get(id=sector.id)

            return Response(
                {
                    "success": True,
                    "message": "Sector created successfully.",
                    "data": SectorSerializer(full_sector).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "message": "Validation error",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# class getAllColors(APIView):
#     permission_classes =[AllowAny]
#     authentication_classes = []
#     def get(self,request):
#         colors = ColorPalete()
        


        

