from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from payment.models import Payment, Interest, DailyInterestAccrual, Balance

class Command(BaseCommand):
    help = 'Apply daily interest to eligible payments'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        count = 0

        eligible_payments = Payment.objects.filter(status='completed', verified_by_admin=True)

        for payment in eligible_payments:
            user = payment.user
            plan = payment.plan
            amount = payment.amount_paid

            # Skip if already applied for this payment today
            if DailyInterestAccrual.objects.filter(payment=payment, date=today).exists():
                continue

            try:
                interest_config = Interest.objects.get(plan=plan)
            except Interest.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"No interest config for plan: {plan}"))
                continue

            percent = interest_config.daily_interest_percent
            daily_interest = (Decimal(percent) / Decimal(100)) * amount

            # Create interest accrual
            DailyInterestAccrual.objects.create(
                user=user,
                payment=payment,
                date=today,
                amount=daily_interest
            )

            # Update balance
            balance, _ = Balance.objects.get_or_create(user=user)
            balance.balance += daily_interest
            balance.save(update_fields=['balance'])

            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully applied interest to {count} payment(s)."))
