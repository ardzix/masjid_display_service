from django.contrib import admin
from .models import (
    User, Mosque, MosqueUser, Subscription,
    Device, Slider, TextMarquee, PrayerTime, MasjidConfiguration
)


# Inline for MosqueUser
class MosqueUserInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = MosqueUser
    extra = 1  # Number of empty rows for adding new users
    fields = ('user', 'role', 'created_at')  # Fields to display in the inline
    readonly_fields = ('created_at',)


# Inline for Device
class DeviceInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = Device
    extra = 1  # Number of empty rows for adding new devices
    fields = ('name', 'device_token', 'is_active', 'last_synced_at', 'created_at')  # Fields to display in the inline
    readonly_fields = ('created_at', 'last_synced_at')


# Mosque Admin
@admin.register(Mosque)
class MosqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'subscription', 'subscription_expiry', 'created_at')
    list_filter = ('subscription',)
    search_fields = ('name', 'address')
    ordering = ('name',)
    inlines = [MosqueUserInline, DeviceInline]  # Add inlines for MosqueUser and Device


# Custom User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_mosque_admin', 'is_device', 'is_staff', 'is_superuser')
    list_filter = ('is_mosque_admin', 'is_device', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)


# Subscription Admin
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_in_days', 'price', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


# Slider Admin
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('mosque', 'background_image', 'text', 'created_at')
    list_filter = ('mosque',)
    search_fields = ('mosque__name', 'text')


# Text Marquee Admin
@admin.register(TextMarquee)
class TextMarqueeAdmin(admin.ModelAdmin):
    list_display = ('mosque', 'text', 'created_at')
    list_filter = ('mosque',)
    search_fields = ('mosque__name', 'text')


# Prayer Time Admin
@admin.register(PrayerTime)
class PrayerTimeAdmin(admin.ModelAdmin):
    list_display = ('mosque', 'date', 'fajr', 'dhuhr', 'asr', 'maghrib', 'isha', 'created_at')
    list_filter = ('mosque', 'date')
    search_fields = ('mosque__name', 'date')


# Masjid Configuration Admin
@admin.register(MasjidConfiguration)
class MasjidConfigurationAdmin(admin.ModelAdmin):
    list_display = ('mosque', 'max_sliders', 'max_text_marquee', 'prayer_duration_days', 'allow_calendar_access', 'created_at')
    list_filter = ('mosque',)
    search_fields = ('mosque__name',)
