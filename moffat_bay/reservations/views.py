# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.shortcuts import render, redirect
from users.forms import MailListForm
from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Stay_Costs, Reservations
from moffat_bay.utilities import *

#reusable method to get all available rooms
def get_available_rooms(checkInDate, checkOutDate):
    overlapping_reservations = Reservations.objects.filter(
                Q(checkInDate__lte=checkInDate, checkOutDate__gt=checkInDate) |
                Q(checkInDate__lt=checkOutDate, checkOutDate__gte=checkOutDate))
    available_rooms = find_available_rooms(checkInDate,checkOutDate, overlapping_reservations)
    return available_rooms


#main landing page view:
def home(request):
    mailform = MailListForm(request.POST or None)
    searchForm = AvailabilityForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!")
            return redirect('reservations-home')
        if searchForm.is_valid(): #add this code to any view with room availability search 
            checkInDate = (searchForm.cleaned_data['checkInDate']).strftime('%Y-%m-%d')
            checkOutDate = (searchForm.cleaned_data['checkOutDate']).strftime('%Y-%m-%d')
            guests = searchForm.cleaned_data['guests']
            return redirect('available_rooms', checkInDate, checkOutDate, guests) 
    context = {
        'title':'Landing Page',
        'mailform': mailform,
        'searchForm': searchForm,
        }
    return render(request, 'reservations/home.html', context)

#about us page view:
def about(request):
    mailform = MailListForm(request.POST or None)
    #add any extra logic needed here
    context = {     #everything in context dictionary gets passed to the html page and used as variables
        'title':'About The Lodge',
        'mailform': mailform,
        #add anything else we want returned and displayed on about page here
        }
    return render(request, 'reservations/about_us.html', context)

#rooms view:
#use for start of booking, reservations, and room overviews
def rooms(request):
    mailform = MailListForm(request.POST or None)
    #add any extra logic/code needed here
    context = {
        'title':'Our Rooms',
        'mailform': mailform,
        #add search availability form here
        #add anything else we want returned and displayed on about page here
        }
    return render(request, 'reservations/rooms.html', context)

#attractions page view:
def attractions(request):
    mailform = MailListForm(request.POST or None)
    #add any extra logic/code needed here
    context = {
        'title':'Local Attractions',
        'mailform': mailform,
        #add search availability form here
        #add anything else we want returned and displayed on about page here
        }
    return render(request, 'reservations/attractions.html', context)

#reservation lookup view:
def reservation_lookup(request):
    mailform = MailListForm(request.POST or None)
    #add any extra logic/code needed here
    context = {
        'title':'My Reservations',
        'mailform': mailform,
        #add search availability form here
        #add anything else we want returned and displayed on about page here
        }
    return render(request, 'reservations/reservation_lookup.html', context)

#book reservations page view"
@login_required(login_url='login')
def book_reservation(request, checkInDate, checkOutDate, guests, roomID):
    nightlyCost = Stay_Costs.objects.filter(guests=guests).get()
    totalCost = get_final_price(nightlyCost.price, checkInDate, checkOutDate, guests)
    nights = get_nights(checkInDate, checkOutDate)
    room = Rooms.objects.filter(roomID=roomID).get()
    context = {
        'title' : f'Reservation summary',
        'nightlyCost': nightlyCost,
        'totalCost': totalCost,
        'guests': guests,
        'checkInDate': checkInDate,
        'checkOutDate': checkOutDate,
        'room': room,
        'nights': nights,
    }

    return render(request, 'reservations/book_reservation.html', context)

def book_now(request):
    if request.method == "POST":
        searchForm = AvailabilityForm(request.POST)
        if searchForm.is_valid(): #add this code to any view with room availability search 
            checkInDate = (searchForm.cleaned_data['checkInDate']).strftime('%Y-%m-%d')
            checkOutDate = (searchForm.cleaned_data['checkOutDate']).strftime('%Y-%m-%d')
            guests = searchForm.cleaned_data['guests']
            return redirect('available_rooms', checkInDate, checkOutDate, guests) 
    else:
        searchForm = AvailabilityForm()
    context = {
        'title':'Start your Reservation',
        'searchForm': searchForm,
        }
    return render(request, 'reservations/start_booking.html', context)

def available_rooms(request, checkInDate, checkOutDate, guests):
    mailform = MailListForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!")
            return redirect('reservations-home')
    context = {
        'title':'Available Rooms',
        'available_rooms': get_available_rooms(checkInDate, checkOutDate),
        'guests': guests,
        'checkInDate': checkInDate,
        'checkOutDate': checkOutDate,
        }
    return render(request, 'reservations/available_rooms.html', context)


#add additional site views here (about, reservations, etc)


#Custom admin page views:
#Nightly Cost Price update by percentage View:
# *** this is located in the admin page****
class NightlyCostPriceUpdateView(FormView):
    form_class = NightlyCostPriceUpdateForm
    template_name = 'reservations/admin/nightly_cost_update.html'
    permission_required = ['user.is_admin']

    def form_valid(self, form):
        percentage = form.cleaned_data['costChange']
        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')
        # Get the selected products
        products = Stay_Costs.objects.filter(id__in=product_ids)
        for product in products:
            product.price = product.price + (product.price * percentage / 100)
            product.save()
        messages.success(self.request, ('Prices updated successfully'))
        return redirect('/admin/reservations/stay_costs')

    def form_invalid(self, form):
        #display error if form is not valid
        messages.error(self.request, ('Error updating prices'))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        #add context data
        context = super().get_context_data(**kwargs)
        context['title'] = ('Update Moffat-Bay Prices')
        context['label'] =('Please enter percentage of price change:')
        context['form_url'] = reverse('price_update')

        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')
        context['stay_costs'] = Stay_Costs.objects.filter(id__in=product_ids)
        return context
    
    #change prices by directly entering the price
class NightlyCostPriceChangeView(FormView):
    form_class = NightlyCostPriceChangeForm
    template_name = 'reservations/admin/nightly_cost_update.html'
    permission_required = ['user.is_admin']

    def form_valid(self, form):
        newCost = form.cleaned_data['costChange']
        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')

        # Get the selected products
        products = Stay_Costs.objects.filter(id__in=product_ids)
        for product in products:
            product.price = newCost
            product.save()
        messages.success(self.request, ('Prices updated successfully'))
        return redirect('/admin/reservations/stay_costs')

    def form_invalid(self, form):
        """
        Display an error message if the form is invalid.
        """
        messages.error(self.request, ('Error updating prices'))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        #add context data
        context = super().get_context_data(**kwargs)
        context['title'] = ('Update Moffat-Bay Prices')
        context['form_url'] = reverse('price_change')
        context['label'] =('Please enter new price:')

        # get product ids from url
        product_ids = self.request.GET.get('id').split(',')
        context['stay_costs'] = Stay_Costs.objects.filter(id__in=product_ids)
        return context
    
