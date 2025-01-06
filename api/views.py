from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Mosque, MosqueUser, Subscription, Device, Slider,
    TextMarquee, MasjidConfiguration
)
from .serializers import (
    MosqueSerializer, MosqueUserSerializer, SubscriptionSerializer,
    DeviceSerializer, SliderSerializer, TextMarqueeSerializer,
    MasjidConfigurationSerializer
)


class BaseMosqueRelatedViewSet(ModelViewSet):
    """
    Base viewset for models related to a Mosque via a ForeignKey.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mosque']  # Ensure filtering by mosque is always required

    def get_queryset(self):
        """
        Restrict queryset to items linked to the current user's mosques and the specified mosque ID.
        """
        queryset = super().get_queryset().filter(
            mosque__mosque_users__user=self.request.user
        )
        mosque_id = self.request.query_params.get('mosque')
        if not mosque_id:
            raise PermissionDenied("The 'mosque' query parameter is required.")
        return queryset.filter(mosque_id=mosque_id)

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
        return Mosque.objects.filter(mosque_users__user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the current user as the admin when registering a new mosque.
        """
        mosque = serializer.save()
        MosqueUser.objects.create(user=self.request.user, mosque=mosque, role='admin')

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """
        Subscribe or buy a package for a mosque.
        """
        mosque = self.get_object()
        subscription_id = request.data.get('subscription_id')
        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except Subscription.DoesNotExist:
            raise PermissionDenied("Invalid subscription ID.")

        if not MosqueUser.objects.filter(user=request.user, mosque=mosque, role='admin').exists():
            raise PermissionDenied("You do not have permission to subscribe for this mosque.")

        # Update mosque subscription and expiry date
        mosque.subscription = subscription
        mosque.subscription_expiry = mosque.created_at + subscription.duration_in_days
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
