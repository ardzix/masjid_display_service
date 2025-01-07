from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from django.utils.timezone import now
from ..models import Device, PrayerTime, Slider, TextMarquee, MasjidConfiguration
from ..serializers import TVContentSerializer


class TVContentViewSet(ViewSet):
    """
    Endpoint to fetch content for TV based on its unique identifier.
    """
    permission_classes = [AllowAny]  # Allow unauthenticated access

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "uuid",
                openapi.IN_QUERY,
                description="The unique identifier of the TV device.",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: TVContentSerializer,
            400: openapi.Response(description="UUID is missing or invalid."),
            404: openapi.Response(description="Device not found.")
        }
    )
    def list(self, request, *args, **kwargs):
        uuid = request.query_params.get('uuid')

        if not uuid:
            return Response({"error": "UUID is required."}, status=400)

        # Find the device by its unique identifier
        try:
            device = Device.objects.select_related('mosque').get(device_token=uuid)
        except Device.DoesNotExist:
            raise NotFound("Device not found.")

        # Fetch related data
        mosque = device.mosque
        today = now().date()

        prayer_schedule = PrayerTime.objects.filter(mosque=mosque, date__gte=today)
        sliders = Slider.objects.filter(mosque=mosque)
        text_marquee = TextMarquee.objects.filter(mosque=mosque)
        configurations = MasjidConfiguration.objects.filter(mosque=mosque).first()

        # Serialize the data
        serializer = TVContentSerializer({
            "mosque": mosque,
            "prayer_schedule": prayer_schedule,
            "sliders": sliders,
            "text_marquee": text_marquee,
            "configurations": configurations
        })

        return Response(serializer.data)
