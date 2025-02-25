from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from datetime import timedelta
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from ..models import (
    Mosque, MosqueUser, Subscription, Device, Slider,
    TextMarquee, MasjidConfiguration
)
from ..serializers import (
    MosqueSerializer, MosqueUserSerializer, SubscriptionSerializer,
    DeviceSerializer, SliderSerializer, TextMarqueeSerializer,
    MasjidConfigurationSerializer
)


# Subscription ID parameter
subscription_id_param = openapi.Parameter(
    "subscription_id", openapi.IN_BODY, description="ID of the subscription package", type=openapi.TYPE_INTEGER
)

# Successful response schema
success_response_schema = openapi.Response(
    description="Subscription updated successfully.",
    examples={
        "application/json": {
            "detail": "Subscription updated successfully."
        }
    },
)

class BaseMosqueRelatedViewSet(ModelViewSet):
    """
    Base viewset for models related to a Mosque via a ForeignKey.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mosque']  # Ensure filtering by mosque is always required

    # Generate the list of filter parameters statically
    mosque_filter_parameters = [
        openapi.Parameter(
            name='mosque',
            in_=openapi.IN_QUERY,
            description='Filter by Mosque ID (Required)',
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ]

    @swagger_auto_schema(manual_parameters=mosque_filter_parameters)
    def list(self, request, *args, **kwargs):
        """
        List items filtered by query parameters.
        """
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Restrict queryset to items linked to the current user's mosques and the specified mosque ID.
        """
        # Handle the case where the user is Anonymous (e.g., when accessing Swagger)
        if not self.request or not self.request.user.is_authenticated:
            return super().get_queryset().none()
        
        queryset = super().get_queryset().filter(
            mosque__mosque_users__user=self.request.user
        )
        if self.action == 'list':
            mosque_id = self.request.query_params.get('mosque')
            if not mosque_id:
                raise PermissionDenied("The 'mosque' query parameter is required.")
            return queryset.filter(mosque_id=mosque_id)
        return queryset

    def perform_create(self, serializer):
        """
        Ensure that the user has admin privileges for the associated mosque.
        """
        mosque = serializer.validated_data.get('mosque')
        if not MosqueUser.objects.filter(user=self.request.user, mosque=mosque, role='admin').exists():
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer.save()


# Mosque ViewSet
class MosqueViewSet(ModelViewSet):
    queryset = Mosque.objects.all()
    serializer_class = MosqueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict queryset to mosques linked to the current user.
        """
        # Handle the case where the user is Anonymous (e.g., when accessing Swagger)
        if not self.request or not self.request.user.is_authenticated:
            return super().get_queryset().none()
        
        return Mosque.objects.filter(mosque_users__user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the current user as the admin when registering a new mosque.
        """
        mosque = serializer.save()
        MosqueUser.objects.create(user=self.request.user, mosque=mosque, role='admin')

    @swagger_auto_schema(
        method="post",
        operation_description="Subscribe or buy a package for a mosque.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "subscription_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the subscription package")
            },
            required=["subscription_id"]
        ),
        responses={
            200: success_response_schema,
            403: "Permission denied. User is not authorized to subscribe.",
            400: "Invalid subscription ID.",
        },
    )
    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """
        Subscribe or buy a package for a mosque.
        """
        mosque = self.get_object()
        subscription_id = request.data.get("subscription_id")
        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "Invalid subscription ID."}, status=status.HTTP_400_BAD_REQUEST)

        if not MosqueUser.objects.filter(user=request.user, mosque=mosque, role='admin').exists():
            raise PermissionDenied("You do not have permission to subscribe for this mosque.")

        # Update the subscription and calculate expiry date
        mosque.subscription = subscription

        # Determine new subscription expiry based on the current logic
        if not mosque.subscription_expiry or mosque.subscription_expiry < now():
            # If no expiry or expiry is in the past
            mosque.subscription_expiry = now() + timedelta(days=subscription.duration_in_days)
        else:
            # If expiry is in the future
            mosque.subscription_expiry += timedelta(days=subscription.duration_in_days)

        mosque.save()

        return Response({"detail": "Subscription updated successfully."})


# Mosque User ViewSet
class MosqueUserViewSet(BaseMosqueRelatedViewSet):
    queryset = MosqueUser.objects.all()
    serializer_class = MosqueUserSerializer


# Slider ViewSet
class SliderViewSet(BaseMosqueRelatedViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


# Text Marquee ViewSet
class TextMarqueeViewSet(BaseMosqueRelatedViewSet):
    queryset = TextMarquee.objects.all()
    serializer_class = TextMarqueeSerializer


# Masjid Configuration ViewSet
class MasjidConfigurationViewSet(BaseMosqueRelatedViewSet):
    queryset = MasjidConfiguration.objects.all()
    serializer_class = MasjidConfigurationSerializer


# Device ViewSet
class DeviceViewSet(BaseMosqueRelatedViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class SubscriptionViewSet(ReadOnlyModelViewSet):
    """
    A ViewSet for listing all subscription details.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]