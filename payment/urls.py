from django.urls import path
from . import views

urlpatterns = [
    path('payment-request/', views.create_payment, name='payment-create'),
    path('payment-history/', views.payment_list, name='payment-list'),
    path('payment-history/<str:payment_id>/', views.payment_detail, name='payment-detail'),
    path('trigger-interest/', views.trigger_interest, name='trigger-interest'),
    path('withdrawals/create/', views.create_withdrawal_request, name='create_withdrawal'),
    path('withdrawals/', views.withdrawal_request_list, name='withdrawal-list'),
    path('balance/', views.user_balance, name='balance-view'),
]
