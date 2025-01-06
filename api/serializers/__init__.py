from rest_framework import serializers
from ..models import (
    User, Mosque, MosqueUser, Subscription,
    Device, Slider, TextMarquee, PrayerTime, MasjidConfiguration
)


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_mosque_admin', 'is_device', 'sso_user_id']
        read_only_fields = ['id']


# Subscription Serializer
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'name', 'duration_in_days', 'benefits', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']


# Device Serializer
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'device_token', 'is_active', 'last_synced_at', 'mosque', 'created_at']
        read_only_fields = ['id', 'last_synced_at', 'created_at']


# Slider Serializer
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'mosque', 'background_image', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


# Text Marquee Serializer
class TextMarqueeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMarquee
        fields = ['id', 'mosque', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


# Prayer Time Serializer
class PrayerTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerTime
        fields = ['id', 'mosque', 'date', 'fajr', 'dhuhr', 'asr', 'maghrib', 'isha', 'created_at']
        read_only_fields = ['id', 'created_at']


# Mosque User Serializer
class MosqueUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested User serializer for detailed user info

    class Meta:
        model = MosqueUser
        fields = ['id', 'user', 'mosque', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


# Masjid Configuration Serializer
class MasjidConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasjidConfiguration
        fields = ['id', 'mosque', 'max_sliders', 'max_text_marquee', 'prayer_duration_days', 'allow_calendar_access', 'created_at']
        read_only_fields = ['id', 'created_at']


# Mosque Serializer
class MosqueSerializer(serializers.ModelSerializer):
    mosque_users = MosqueUserSerializer(many=True, read_only=True)  # Include mosque users inline
    devices = DeviceSerializer(many=True, read_only=True)  # Include devices inline

    class Meta:
        model = Mosque
        fields = [
            'id', 'name', 'address', 'latitude', 'longitude', 'subscription',
            'subscription_expiry', 'created_at', 'mosque_users', 'devices'
        ]
        read_only_fields = ['id', 'created_at']
