from django.urls import path
from . import views



urlpatterns = [
    path('referral-details/', views.get_referral_details, name='referral-details'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
    path('contact/', views.create_contact, name='create_contact'),


]


