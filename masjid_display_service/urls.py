from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.contrib import admin
from api.views import (
    MosqueViewSet, MosqueUserViewSet,
    SliderViewSet, TextMarqueeViewSet, MasjidConfigurationViewSet,
    SubscriptionViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'mosques', MosqueViewSet, basename='mosque')
router.register(r'mosque-users', MosqueUserViewSet, basename='mosqueuser')
router.register(r'sliders', SliderViewSet, basename='slider')
router.register(r'text-marquees', TextMarqueeViewSet, basename='textmarquee')
router.register(r'configurations', MasjidConfigurationViewSet, basename='masjidconfiguration')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Masjid Display Service API",
        default_version="v1",
        description="API documentation for managing mosques, users, subscriptions, and configurations.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@masjidservice.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),  # Allow public access to the documentation
)

# Include the router's URLs and documentation endpoints
urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
]
