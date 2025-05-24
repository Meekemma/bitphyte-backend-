from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import *

registration_swagger = swagger_auto_schema(
    method='post',
    operation_summary="User Registration",
    operation_description="This endpoint registers a new user by email, first name, last name, and password.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'first_name', 'last_name', 'password', 'password2'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='user@example.com'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='John'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Doe'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', example='strongPassword123'),
            'password2': openapi.Schema(type=openapi.TYPE_STRING, format='password', example='strongPassword123'),
        },
    ),
    responses={
        201: openapi.Response(
            description="User registered successfully.",
            examples={
                "application/json": {
                    "message": "User created successfully!",
                    "data": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Validation error occurred.",
            examples={
                "application/json": {
                    "email": ["A user with this email already exists."],
                    "password": ["Passwords do not match."]
                }
            }
        )
    },
    tags=["Authentication"],
)








login_swagger = swagger_auto_schema(
    method='post',
    operation_summary="User Login",
    operation_description="Authenticate user with email and password to receive JWT tokens or session.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='user@example.com'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', example='strongPassword123'),
        },
    ),
    responses={
        200: openapi.Response(
            description="User logged in successfully.",
            examples={
                "application/json": {
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                }
            }
        ),
        400: openapi.Response(
            description="Invalid credentials or validation errors.",
            examples={
                "application/json": {
                    "non_field_errors": ["Invalid credentials."]
                }
            }
        )
    },
    tags=["Authentication"],
)



verify_otp_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Verify OTP Code",
    operation_description="Verify a 6-digit OTP code sent to the user email.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['code'],
        properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING, max_length=6, min_length=6, example='123456'),
        }
    ),
    responses={
        200: openapi.Response(
            description="OTP verified successfully.",
            examples={
                "application/json": {"message": "OTP verified, user activated."}
            }
        ),
        400: openapi.Response(
            description="Invalid or expired OTP.",
            examples={
                "application/json": {
                    "code": ["Invalid OTP code"],
                }
            }
        )
    },
    tags=["Authentication"],
)



resend_otp_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Resend OTP",
    operation_description="Request a new OTP to be sent to the user's email.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='user@example.com'),
        }
    ),
    responses={
        200: openapi.Response(
            description="OTP resent successfully.",
            examples={
                "application/json": {"message": "A new OTP has been sent to your email."}
            }
        ),
        400: openapi.Response(
            description="Validation error or rate limit exceeded.",
            examples={
                "application/json": {
                    "email": ["User does not exist or rate limit exceeded."]
                }
            }
        )
    },
    tags=["Authentication"],
)



logout_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Logout User",
    operation_description="Blacklist refresh token to logout user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, example='refresh_token_here'),
        }
    ),
    responses={
        204: openapi.Response(description="Logout successful, token blacklisted."),
        400: openapi.Response(
            description="Invalid or expired token.",
            examples={
                "application/json": {"refresh": ["Invalid or expired refresh token"]}
            }
        )
    },
    tags=["Authentication"],
)




password_reset_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Password Reset Request",
    operation_description="Request password reset email if user exists and is verified.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='user@example.com'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Password reset email sent.",
            examples={
                "application/json": {"message": "Password reset instructions sent to your email."}
            }
        ),
        400: openapi.Response(
            description="Validation error or rate limiting.",
            examples={
                "application/json": {
                    "email": ["No user found with this email address", "User email is not verified", "Please wait 60 seconds before requesting another password reset"]
                }
            }
        )
    },
    tags=["Authentication"],
)


user_profile_swagger = swagger_auto_schema(
    method='get',
    operation_summary="Get User Profile",
    operation_description="Retrieve user profile information.",
    responses={
        200: openapi.Response(
            description="User profile data retrieved.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='John'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Doe'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='user@example.com'),
                    'gender': openapi.Schema(type=openapi.TYPE_STRING, example='male'),
                    'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example='+1234567890'),
                    'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format='url', example='http://example.com/media/profile.jpg'),
                    'country': openapi.Schema(type=openapi.TYPE_STRING, example='USA'),
                    'address': openapi.Schema(type=openapi.TYPE_STRING, example='123 Main St'),
                    'city': openapi.Schema(type=openapi.TYPE_STRING, example='New York'),
                    'state': openapi.Schema(type=openapi.TYPE_STRING, example='NY'),
                    'referral_code': openapi.Schema(type=openapi.TYPE_STRING, example='ABC123'),
                    'referral_url': openapi.Schema(type=openapi.TYPE_STRING, format='url', example='http://example.com/referral/ABC123'),
                }
            )
        )
    },
    tags=["User Profile"],
)





update_profile_put_swagger = swagger_auto_schema(
    method='put',
    operation_summary="Fully Update User Profile",
    operation_description="Replace the user's profile with all new data. All fields should be provided.",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('gender', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, example="male"),
        openapi.Parameter('phone_number', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, example="+2348123456789"),
        openapi.Parameter('country', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, example="Nigeria"),
        openapi.Parameter('address', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, example="23B Adeola Odeku"),
        openapi.Parameter('city', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, example="Lagos"),
        openapi.Parameter('state', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, example="Lagos"),
        openapi.Parameter('profile_picture', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False, description="Profile image upload"),
    ],
    responses={
        200: openapi.Response(description="Profile fully updated successfully"),
        400: openapi.Response(description="Validation error"),
        404: openapi.Response(description="User not found"),
    },
    tags=["User Profile"],
)



update_profile_patch_swagger = swagger_auto_schema(
    method='patch',
    operation_summary="Partially Update User Profile",
    operation_description="Update selected fields of the user's profile.",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('gender', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('phone_number', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('country', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('address', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('city', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('state', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('profile_picture', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
    ],
    responses={
        200: openapi.Response(description="Profile partially updated successfully"),
        400: openapi.Response(description="Validation error"),
        404: openapi.Response(description="User not found"),
    },
    tags=["User Profile"],
)
