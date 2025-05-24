# docs/swagger_docs.py

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import PaymentSerializer, WithdrawalRequestSerializer

# Swagger for creating a new payment
create_payment_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Create payment",
    operation_description="Create a new payment for a plan. Automatically assigns the authenticated user.",
    request_body=PaymentSerializer,
    responses={
        201: openapi.Response(
            description="Payment created successfully",
            schema=PaymentSerializer
        ),
        400: openapi.Response(
            description="Validation failed",
            examples={
                "application/json": {
                    "plan": ["Invalid plan selected."],
                    "amount_paid": ["Minimum amount for the Starter plan is 100."]
                }
            }
        )
    }
)

# Swagger for retrieving payment history
list_payments_swagger = swagger_auto_schema(
    method='get',
    operation_summary="List payments",
    operation_description="Retrieve a list of all payments made by the authenticated user.",
    responses={
        200: openapi.Response(
            description="List of payments retrieved",
            schema=PaymentSerializer(many=True)
        )
    }
)

# Swagger for creating a withdrawal request
create_withdrawal_swagger = swagger_auto_schema(
    method='post',
    operation_summary="Request withdrawal",
    operation_description="Request a withdrawal from the user's available balance.",
    request_body=WithdrawalRequestSerializer,
    responses={
        201: openapi.Response(
            description="Withdrawal request created successfully",
            schema=WithdrawalRequestSerializer
        ),
        400: openapi.Response(
            description="Validation failed",
            examples={
                "application/json": {
                    "amount": ["You do not have enough balance to withdraw."],
                    "non_field_errors": ["You cannot withdraw more than your available balance."]
                }
            }
        )
    },
    tags=["Withdrawals"]
)

# Swagger for retrieving user's withdrawal requests
list_withdrawals_swagger = swagger_auto_schema(
    method='get',
    operation_summary="List withdrawals",
    operation_description="Retrieve a list of the user's previous withdrawal requests.",
    responses={
        200: openapi.Response(
            description="List of withdrawal requests",
            schema=WithdrawalRequestSerializer(many=True)
        )
    },
    tags=["Withdrawals"]
)
