from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from .models import Profile
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    """
    API endpoint that permits raw unauthenticated instantiation of a system User identities.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class VerifyEmailView(APIView):
    """
    Consumes wildcard UUIDs bridging the React interface and physically flags the matching Profile.
    """
    permission_classes = (AllowAny,)
    
    def get(self, request, token):
        try:
            profile = Profile.objects.get(verification_token=token)
            if profile.is_verified:
                return Response({"message": "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)
                
            profile.is_verified = True
            profile.save()
            return Response({"message": "Successfully verified email."}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Invalid verification token."}, status=status.HTTP_404_NOT_FOUND)
