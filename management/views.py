from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ReferralSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import *
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_referral_details(request):
    """
    Retrieves referral details for the authenticated user.
    """
    try:
        user_profile = request.user.userprofile
        referrals = Referral.objects.filter(referrer=user_profile)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

    if not referrals.exists():
        return Response({"message": "No referrals yet."}, status=status.HTTP_200_OK)

    serializer = ReferralSerializer(referrals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
