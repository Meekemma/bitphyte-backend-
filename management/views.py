from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ReferralSerializer,SubscriberSerializer,ContactSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
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







@api_view(['POST'])
def subscribe(request):
    serializer = SubscriberSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        subscriber = serializer.save()  
        return Response({"message": "Subscription successful!", "email": subscriber.email}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def unsubscribe(request, email):
    subscriber = get_object_or_404(Subscriber, email__iexact=email)
    if subscriber.is_active:
        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()
        return Response({'message': 'You have successfully unsubscribed.'})
    return Response({'message': 'You are already unsubscribed.'}, status=400)





 

@api_view(['POST'])
def create_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # calls create() in serializer
        return Response(
            {"message": "Thank you for reaching out. We'll get back to you soon."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

