from django.contrib import admin

from .models import *


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('code', 'referrer', 'referee', 'status', 'bonus', 'referred_at')
    list_filter = ('status', 'referred_at')
    search_fields = ('code', 'referrer__user__first_name', 'referee__user__first_name')
    autocomplete_fields = ('referrer', 'referee')
    readonly_fields = ('referred_at',)



@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active', 'unsubscribed_at')
    search_fields = ('email',)
    list_filter = ('is_active', 'subscribed_at', 'unsubscribed_at')





@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)

