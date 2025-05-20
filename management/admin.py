from django.contrib import admin

from .models import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('code', 'referrer', 'referee', 'status', 'bonus', 'referred_at')
    list_filter = ('status', 'referred_at')
    search_fields = ('code', 'referrer__user__first_name', 'referee__user__first_name')
    autocomplete_fields = ('referrer', 'referee')
    readonly_fields = ('referred_at',)
