from rest_framework import serializers
from .models import UserAuth
import requests
from rest_framework import serializers
from decouple import config
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .accounts_utils import validate_facebook_token, validate_google_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = ['id', 'email', 'full_name', 'profile_pic' , 'occupation', 'mobile_no', 'location', 'is_verified','date_joined', 'updated_at']
        read_only_fields = ['id', 'email', 'is_verified']
        
        
# SOCAIL AUTH

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserAuth
from .serializers import UserSerializer  # Update to your actual user serializer path
from .accounts_utils import validate_google_token  # Adjust path if needed

class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate(self, attrs):
        id_token = attrs.get("id_token")
        print("ID Token:", id_token)  # Debugging line

        google_data = validate_google_token(id_token)
        print("Google data:", google_data)  # Debugging line

        if not google_data or not google_data.get("email"):
            raise serializers.ValidationError("Invalid Google token or missing email.")

        try:
            user, created = UserAuth.objects.get_or_create(
                email=google_data["email"],
                defaults={
                    "full_name": google_data.get("name", ""),
                },
            )
        except Exception:
            raise serializers.ValidationError("Could not create or retrieve user.")

        if created:
            user.set_unusable_password()
            user.is_verified = True
            user.save()

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_profile": UserSerializer(user).data,
        }



        
        
class FacebookAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get("access_token")

        facebook_data = validate_facebook_token(access_token)

        if not facebook_data or not facebook_data.get("email"):
            raise serializers.ValidationError("Invalid Facebook token or missing email.")

        try:
            user, created = UserAuth.objects.get_or_create(
                email=facebook_data["email"],
                defaults={
                    "full_name": facebook_data.get("name", ""),
                },
            )
        except Exception:
            raise serializers.ValidationError("Could not create or retrieve user.")

        if created:
            user.set_unusable_password()
            user.is_verified = True
            user.save()

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_profile": UserSerializer(user).data
        }
