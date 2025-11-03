from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RequestOTPSerializer, VerifyOTPSerializer
from .utils import create_and_send_otp_code
from .models import EmailOTP

User = get_user_model()

class RequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower().strip()
        otp = create_and_send_otp_code(email)
        # Do not return OTP; return a minimal success response
        return Response({"detail": "OTP sent if email is valid"}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower().strip()
        code = serializer.validated_data["code"].strip()

        # Find matching unused OTP
        try:
            otp = EmailOTP.objects.filter(email=email, code=code, used=False).latest("created_at")
        except EmailOTP.DoesNotExist:
            return Response({"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            return Response({"detail": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Mark used (atomic update recommended in heavy load)
        otp.used = True
        otp.save(update_fields=["used"])

        # Get or create user for this email
        user, created = User.objects.get_or_create(username=email, defaults={"email": email})
        # You may want to set is_active or other fields depending on your auth strategy

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.pk,
                "email": user.email,
            }
        }, status=status.HTTP_200_OK)
