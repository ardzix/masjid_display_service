from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class SSOAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Authenticate user based on sso_user_id from token.
        """
        raw_token = self.get_raw_token(self.get_header(request))
        if not raw_token:
            return None

        validated_token = self.get_validated_token(raw_token)
        # print(validated_token)
        sso_user_id = validated_token.get("user_id")

        if not sso_user_id:
            raise AuthenticationFailed("Invalid token: 'user_id' not found.")

        # Get or create user based on sso_user_id
        user, created = User.objects.get_or_create(sso_user_id=sso_user_id, defaults={
            "username": f"user_{sso_user_id}",  # Assign a default username
            "email": "",  # Optional: you can update later if needed
        })

        return user, validated_token
