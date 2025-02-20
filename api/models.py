
from django.db import models
from django.contrib.auth.models import AbstractUser
from libs.storage import FILE_STORAGE
from common.models import File
import datetime


class User(AbstractUser):
    is_mosque_admin = models.BooleanField(default=False)  # Indicates if this user is a mosque admin
    is_device = models.BooleanField(default=False)  # Indicates if this user is a device
    sso_user_id = models.UUIDField(unique=True, null=True, blank=True)  

    # Resolve conflicts by explicitly setting related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Avoids conflict with the default related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Avoids conflict with the default related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Mosque Model
class Mosque(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscribed_mosques'
    )
    subscription_expiry = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_subscription_active(self):
        """
        Check if the mosque's subscription is still active.
        """
        return self.subscription_expiry and self.subscription_expiry >= datetime.date.today()

    def __str__(self):
        return self.name


# Role Assignment for Mosque Users
class MosqueUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mosque_roles")
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name="mosque_users")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'mosque')  # Prevent the same user from being added multiple times to the same mosque

    def __str__(self):
        return f"{self.user.username} - {self.mosque.name} ({self.role})"


# Subscription Model
class Subscription(models.Model):
    name = models.CharField(max_length=100)
    duration_in_days = models.IntegerField()  # Duration of the subscription in days
    benefits = models.JSONField(default=dict)  # Store benefits like slider count, etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Device Model
class Device(models.Model):
    name = models.CharField(max_length=255)
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name="devices")
    device_token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    sso_device_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Optional link to SSO
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Slider Model
class Slider(models.Model):
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name="sliders")
    background_image = models.ForeignKey(File, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slider for {self.mosque.name}"


# Text Marquee Model
class TextMarquee(models.Model):
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name="text_marquees")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Text Marquee for {self.mosque.name}"


# Prayer Time Model
class PrayerTime(models.Model):
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name="prayer_times")
    date = models.DateField()
    imsak = models.TimeField()
    fajr = models.TimeField()
    sunrise = models.TimeField()
    dhuhr = models.TimeField()
    asr = models.TimeField()
    sunset = models.TimeField()
    maghrib = models.TimeField()
    isha = models.TimeField()
    midnight = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)


# Masjid Configuration Model
class MasjidConfiguration(models.Model):
    mosque = models.OneToOneField(Mosque, on_delete=models.CASCADE, related_name="configuration")
    max_sliders = models.IntegerField(default=5)
    max_text_marquee = models.IntegerField(default=3)
    prayer_duration_days = models.IntegerField(default=30)  # Number of days prayer times will be generated
    allow_calendar_access = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

from auditlog.registry import auditlog

# Register models for auditing
auditlog.register(Mosque)
auditlog.register(MosqueUser)
auditlog.register(Subscription)
auditlog.register(Device)
auditlog.register(Slider)
auditlog.register(TextMarquee)
auditlog.register(PrayerTime)
auditlog.register(MasjidConfiguration)
