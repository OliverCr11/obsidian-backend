from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from .utils import send_verification_email

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        # We enforce email to serve dually as the unique username
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        
        # Generate exact 1-to-1 secure Profile
        profile = Profile.objects.create(user=user)
        
        # Dispatch Resend Auth Email asynchronously (standard block for MVP)
        send_verification_email(user, profile)
        
        return user
