# docs/swagger_docs.py

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ReferralSerializer, SubscriberSerializer, ContactSerializer

referral_details_swagger = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve referral details",
    operation_description="Get referral information for the authenticated user including bonus and referred users.",
    responses={
        200: openapi.Response(
            description="Referral details retrieved successfully",
            schema=ReferralSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "code": "ABC123",
                        "referee": 2,
                        "referrer": 1,
                        "status": "pending",
                        "bonus": "0.00",
                        "referred_at": "2025-05-24T12:00:00Z",
                        "referee_count": 5,
                        "referral_bonus": "25.00",
                        "referee_details": {
                            "email": "ref@example.com",
                            "full_name": "Ref User",
                            "status": "pending",
                            "bonus": "0.00",
                            "referred_at": "2025-05-24T12:00:00Z"
                        }
                    }
                ]
            }
        ),
        404: 'User profile not found'
    },
    tags=["Referrals"]
)

subscribe_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Subscribe user",
    operation_description="Subscribe a user to the newsletter with an email address.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='subscriber@example.com')
        }
    ),
    responses={
        201: openapi.Response(
            description="Subscription successful",
            examples={
                "application/json": {
                    "message": "Subscription successful!",
                    "email": "subscriber@example.com"
                }
            }
        ),
        400: "Bad Request"
    },
    tags=["Subscribers"]
)

unsubscribe_swagger = swagger_auto_schema(
    method='get',
    operation_summary="Unsubscribe user",
    operation_description="Unsubscribe a user using their email address.",
    manual_parameters=[
        openapi.Parameter('email', openapi.IN_PATH, description="Email address to unsubscribe", type=openapi.TYPE_STRING)
    ],
    responses={
        200: openapi.Response(
            description="Successfully unsubscribed",
            examples={
                "application/json": {
                    "message": "You have successfully unsubscribed."
                }
            }
        ),
        400: openapi.Response(
            description="Already unsubscribed",
            examples={
                "application/json": {
                    "message": "You are already unsubscribed."
                }
            }
        )
    },
    tags=["Subscribers"]
)

contact_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Create contact message",
    operation_description="Submit a contact form with name, email, and message.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'email', 'message'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, example='John Doe'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='john@example.com'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, example='I need help with your service. Please get back to me as soon as possible.')
        }
    ),
    responses={
        201: openapi.Response(
            description="Contact created successfully",
            examples={
                "application/json": {
                    "message": "Thank you for reaching out. We'll get back to you soon."
                }
            }
        ),
        400: "Bad Request"
    },
    tags=["Contact"]
)
