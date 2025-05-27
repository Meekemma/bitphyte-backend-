from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal
from .serializers import PaymentSerializer,WithdrawalRequestSerializer,BalanceSerializer
from .swagger_docs import create_payment_swagger,list_payments_swagger,create_withdrawal_swagger
from .models import *



@create_payment_swagger
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    serializer = PaymentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message": "Payment created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@list_payments_swagger
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_list(request):
    payments = Payment.objects.only(
        'user', 'plan', 'amount_paid', 'transaction_id', 'status', 'created_at'
    ).filter(user=request.user).order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, user=request.user)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
# @permission_classes([IsAdminUser])
def trigger_interest(request):
    today = timezone.now().date()
    count = 0

    eligible_payments = Payment.objects.filter(status='completed', verified_by_admin=True)

    for payment in eligible_payments:
        user = payment.user
        plan = payment.plan
        amount = payment.amount_paid

        if DailyInterestAccrual.objects.filter(user=user, date=today, payment=payment).exists():
            continue

        try:
            interest_config = Interest.objects.get(plan=plan)
        except Interest.DoesNotExist:
            continue

        percent = interest_config.daily_interest_percent
        daily_interest = (Decimal(percent) / 100) * amount

        DailyInterestAccrual.objects.create(user=user, date=today, amount=daily_interest, payment=payment)

        balance, _ = Balance.objects.get_or_create(user=user)
        balance.balance += daily_interest
        balance.save(update_fields=['balance'])

        count += 1

    return Response({"message": f"Interest applied to {count} users."})






@create_withdrawal_swagger
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_withdrawal_request(request):
    serializer = WithdrawalRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        try:
            withdrawal = serializer.save(user=request.user)
            # Run model clean validation
            withdrawal.full_clean()
            withdrawal.save()
            return Response(WithdrawalRequestSerializer(withdrawal).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def withdrawal_request_list(request):
    withdrawals = WithdrawalRequest.objects.filter(user=request.user).order_by('-created_at')
    serializer = WithdrawalRequestSerializer(withdrawals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_balance(request):
    balance = get_object_or_404(Balance, user=request.user)
    serializer = BalanceSerializer(balance)
    return Response(serializer.data, status=status.HTTP_200_OK)