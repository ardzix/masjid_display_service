import requests
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from django.utils.timezone import now
from .models import Mosque, Subscription, MosqueUser, Slider, TextMarquee, Device, MasjidConfiguration, User

class MasjidDisplayServiceTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Authenticate with SSO to get access token
        sso_url = "https://sso.arnatech.id/api/auth/login/"
        sso_credentials = {
            "email": "ardzyix@gmail.com",
            "password": "Barakadut1234!"
        }
        response = requests.post(sso_url, json=sso_credentials)
        if response.status_code != 200:
            raise Exception("Failed to authenticate with SSO")
        cls.access_token = response.json()["access"]

    def setUp(self):
        # Set Authorization header with the access token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Create test data
        self.subscription = Subscription.objects.create(
            name="Basic Plan",
            duration_in_days=30,
            benefits="Basic benefits",
            price=10000
        )

        self.mosque = Mosque.objects.create(
            name="Test Mosque",
            address="123 Test St",
            latitude=0.0,
            longitude=0.0,
        )

        self.slider = Slider.objects.create(
            mosque=self.mosque,
            # background_image="slider_image.jpg",
            text="Welcome to the Mosque"
        )

        self.text_marquee = TextMarquee.objects.create(
            mosque=self.mosque,
            text="Upcoming Events"
        )

        self.device = Device.objects.create(
            mosque=self.mosque,
            name="Main Hall Display",
            device_token="sample-device-token"
        )

        self.config = MasjidConfiguration.objects.create(
            mosque=self.mosque,
            max_sliders=5,
            max_text_marquee=3,
            prayer_duration_days=30,
            allow_calendar_access=True
        )

    def test_list_mosques(self):
        response = self.client.get("/api/mosques/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Mosque", str(response.data))

    def test_create_mosque(self):
        payload = {
            "name": "New Mosque",
            "address": "789 New St",
            "latitude": 10.0,
            "longitude": 20.0
        }
        response = self.client.post("/api/mosques/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mosque.objects.count(), 2)

    def test_subscribe_to_mosque(self):
        response = self.client.post(
            f"/api/mosques/{self.mosque.id}/subscribe/",
            {"subscription_id": self.subscription.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mosque.refresh_from_db()
        self.assertEqual(self.mosque.subscription, self.subscription)
        self.assertIsNotNone(self.mosque.subscription_expiry)

    def test_list_sliders(self):
        response = self.client.get(f"/api/sliders/?mosque={self.mosque.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Welcome to the Mosque", str(response.data))

    def test_create_slider(self):
        payload = {
            "mosque": self.mosque.id,
            "text": "Ramadan Mubarak"
        }
        response = self.client.post("/api/sliders/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Slider.objects.count(), 2)

    def test_list_text_marquees(self):
        response = self.client.get(f"/api/text-marquees/?mosque={self.mosque.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Upcoming Events", str(response.data))

    def test_create_text_marquee(self):
        payload = {
            "mosque": self.mosque.id,
            "text": "New Event Announcement"
        }
        response = self.client.post("/api/text-marquees/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TextMarquee.objects.count(), 2)

    def test_list_configurations(self):
        response = self.client.get(f"/api/configurations/?mosque={self.mosque.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("max_sliders", str(response.data))

    def test_list_subscriptions(self):
        response = self.client.get("/api/subscriptions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Basic Plan", str(response.data))
