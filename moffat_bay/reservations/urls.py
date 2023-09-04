from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='reservations-home'),
    path('about-moffat-bay-lodge/', views.about, name='about_us'),
    path('our-rooms/', views.rooms, name='rooms'),
    #add remaining site pages urls here

    #additional admin page urls
    path("lodge-admin/update-pricing/", views.NightlyCostPriceUpdateView.as_view(), name="price_update"),
    path("lodge-admin/change-pricing/", views.NightlyCostPriceChangeView.as_view(), name="price_change"),

]
