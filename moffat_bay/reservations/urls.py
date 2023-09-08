# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.urls import path, register_converter
from . import views
from decimal import *

class DecimalConverter:
    regex = r'[-+]?\d*\.\d+|\d+'

    def to_python(self, value):
        return Decimal(value)

    def to_url(self, value):
        return str(value)

register_converter(DecimalConverter, 'decimal')

urlpatterns = [
    path('', views.home, name='reservations-home'),
    path('about-moffat-bay-lodge/', views.about, name='about_us'),
    path('our-rooms/', views.rooms, name='rooms'),
    path('local-attractions/', views.attractions, name='attractions'),
    path('my-reservations/', views.reservation_lookup, name='reservation_lookup'),
    path('start-booking/', views.book_now, name='book_now'),
    path('available-rooms/<str:checkInDate>/<str:checkOutDate>/<int:guests>/', views.available_rooms, name='available_rooms'),
    path('book-reservation/<str:checkInDate>/<str:checkOutDate>/<int:guests>/<int:roomID>/', views.book_reservation, name='book-reservation'),
    path('reservation-confirmation/<str:checkInDate>/<str:checkOutDate>/<int:guests>/<int:roomID>/<decimal:totalCost>/', 
                views.booking_confirmed, name='reservation_confirmation'),
    path('book-room/<int:size>', views.book_room, name='book_room'),
    
    
    #add remaining site pages urls here

    #additional admin page urls
    path("lodge-admin/update-pricing/", views.NightlyCostPriceUpdateView.as_view(), name="price_update"),
    path("lodge-admin/change-pricing/", views.NightlyCostPriceChangeView.as_view(), name="price_change"),

]
