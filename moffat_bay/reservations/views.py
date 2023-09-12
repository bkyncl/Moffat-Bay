# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.shortcuts import render, redirect
from users.forms import MailListForm, ContactForm
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Stay_Costs, Reservations
from moffat_bay.utilities import *
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

#reusable method to get all available rooms
def get_available_rooms(checkInDate, checkOutDate):
    overlapping_reservations = Reservations.objects.filter(
                Q(checkInDate__lte=checkInDate, checkOutDate__gt=checkInDate) |
                Q(checkInDate__lt=checkOutDate, checkOutDate__gte=checkOutDate))
    available_rooms = find_available_rooms(checkInDate,checkOutDate, overlapping_reservations)
    return available_rooms

#get available rooms method, with size choice:
def alt_get_available_rooms(checkInDate, checkOutDate, size):
    overlapping_reservations = Reservations.objects.filter(
                Q(checkInDate__lte=checkInDate, checkOutDate__gt=checkInDate) |
                Q(checkInDate__lt=checkOutDate, checkOutDate__gte=checkOutDate))
    available_rooms = alt_find_available_rooms(checkInDate,checkOutDate, overlapping_reservations, size)
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
    # Create instances of both forms
    mailform = MailListForm(request.POST or None)
    contact_form = ContactForm(request.POST or None)

    if request.method == "POST":
        if 'mailform_submit' in request.POST:
            # Handle the MailListForm submission
            if mailform.is_valid():
                mailform.save()
                messages.success(request, "Thank you for signing up for our mailing list!")
                return redirect('about_us')
        elif 'contact_form_submit' in request.POST:
            # Handle the ContactForm submission
            if contact_form.is_valid():
                # Get form data
                name = contact_form.cleaned_data["name"]
                email = contact_form.cleaned_data["email"]
                message = contact_form.cleaned_data["message"]

                # Create a dictionary with the contact form data
                contact_data = {
                    'name': name,
                    'email': email,
                    'message': message,
                }

                # Send the contact form email
                # Send the contact form email
                if send_contact_email(contact_data):
                    messages.success(request, "Your message has been sent!")  # Display success message
                    #i tried to have it redirect to the #contact-from div here but could not determine a simple way
                    #will look into more simple options....
                else:
                    messages.error(request, "Failed to send your message. Please try again.")  # Display error message
    context = {
        'title': 'Contact Us',
        'mailform': mailform,
        'contact_form': contact_form,  # Add the contact form to the context
        # Add anything else you want to be returned and displayed on the contact us page here
    }
    return render(request, 'reservations/about_us.html', context)

#contact us page view with both MailListForm and ContactForm: 
def contact_us(request):
    # Create instances of both forms
    mailform = MailListForm(request.POST or None)
    contact_form = ContactForm(request.POST or None)

    if request.method == "POST":
        if 'mailform_submit' in request.POST:
            # Handle the MailListForm submission
            if mailform.is_valid():
                mailform.save()
                messages.success(request, "Thank you for signing up for our mailing list!")
                return redirect('contact_us')
        elif 'contact_form_submit' in request.POST:
            # Handle the ContactForm submission
            if contact_form.is_valid():
                # Get form data
                name = contact_form.cleaned_data["name"]
                email = contact_form.cleaned_data["email"]
                message = contact_form.cleaned_data["message"]

                # Create a dictionary with the contact form data
                contact_data = {
                    'name': name,
                    'email': email,
                    'message': message,
                }

                # Send the contact form email
                # Send the contact form email
                if send_contact_email(contact_data):
                    messages.success(request, "Your message has been sent!")  # Display success message
                else:
                    messages.error(request, "Failed to send your message. Please try again.")  # Display error message


    context = {
        'title': 'Contact Us',
        'mailform': mailform,
        'contact_form': contact_form,  # Add the contact form to the context
        # Add anything else you want to be returned and displayed on the contact us page here
    }
    return render(request, 'reservations/contact_us.html', context)

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
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!")
            return redirect('attractions')
    context = {
        'title':'Local Attractions',
        'mailform': mailform,
        #add search availability form here
        #add anything else we want returned and displayed on about page here
        }
    return render(request, 'reservations/attractions.html', context)

#reservation lookup view:
@login_required
def reservation_lookup(request, *args, **kwargs):
    mailform = MailListForm(request.POST or None)
    mySearchForm = MyReservationSearchForm(request.POST or None)
    context = {
        'title':'My Reservations',
        'mailform': mailform,
        'mySearchForm': mySearchForm,
        }
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!")
            return redirect(request)
        if mySearchForm.is_valid():
            searchValue = mySearchForm.cleaned_data['searchConfirm']
            

    else:
        context.update({'myReservation': Reservations.objects.filter(reservationID=1011)})

    return render(request, 'reservations/reservation_lookup.html', context)

#book reservations page view:
@login_required
def book_reservation(request, checkInDate, checkOutDate, guests, roomID):
    nightlyCost = Stay_Costs.objects.filter(guests=guests).get()
    totalCost = get_final_price(nightlyCost.price, checkInDate, checkOutDate, guests)
    nights = get_nights(checkInDate, checkOutDate)
    room = Rooms.objects.filter(roomID=roomID).get()
    userid = request.user.id
    # ADD MAILIST FORM & LOGIC **************************************
    context = {
        'title' : f'Reservation summary',
        'nightlyCost': nightlyCost,
        'totalCost': totalCost,
        'guests': guests,
        'checkInDate': checkInDate,
        'checkOutDate': checkOutDate,
        'room': room,
        'nights': nights,
        'user':userid,
    }
    return render(request, 'reservations/book_reservation.html', context)


def book_now(request):
    if request.method == "POST":
        searchForm = AvailabilityForm(request.POST)
        mailform = MailListForm(request.POST)
        if searchForm.is_valid(): 
            checkInDate = searchForm.cleaned_data['checkInDate']
            checkOutDate = searchForm.cleaned_data['checkOutDate']
            inputdate = datetime.strptime(str(checkInDate), '%Y-%m-%d')
            # Perform date validation 
            if checkOutDate <= checkInDate:     #if check-out is before check-in
                messages.error(request, "Error: Check-out date must be AFTER check-in date. Please try again.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if checkInDate < date.today():  #if check-in date is in the past
                messages.error(request, "Error: Check-in date cannot be in the past. Please try again.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if (inputdate - datetime.now()).days > 365:
                messages.error(request, "We are sorry, Moffat-Bay Marina & Lodge does not accept reservations for more than a year in advance. Please come back soon to book your stay!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #if no date validation errors:
            guests = searchForm.cleaned_data['guests']
            checkInDate = checkInDate.strftime('%Y-%m-%d')
            checkOutDate = checkOutDate.strftime('%Y-%m-%d')
            
            return redirect('available_rooms', checkInDate, checkOutDate, guests) 
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!")
            return redirect('book_now')
    
    else:
        searchForm = AvailabilityForm()
        mailform = MailListForm()
    context = {
        'title':'Start your Reservation',
        'searchForm': searchForm,
        'mailform': mailform,
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

@login_required
def booking_confirmed(request, checkInDate, checkOutDate, guests, roomID, totalCost):
    confirmationKey = generate_confirmation_code(checkInDate, checkOutDate, guests, roomID)
    userId = request.user
    room = Rooms.objects.filter(roomID=roomID).get()
    newReservation = Reservations(confirmationKey=confirmationKey, userID=userId, roomID=room, guests=guests, 
                                  totalPrice=totalCost, checkInDate=checkInDate, checkOutDate=checkOutDate)
    newReservation.save()
    confirm = Reservations.objects.filter(userID=userId, checkInDate=checkInDate, checkOutDate=checkOutDate).get()
    # ADD MAILLIST FORM AND HANDLING *********************************
    context = {
        'title': 'Reservation Confirmation',
        'reservation': confirm
    }
    send_email_confirmation(confirm)
    return render(request, 'reservations/book_reservation_confirmation.html',context)

#alternate booking pathway:
def book_room(request, size):
    if request.method == "POST":
        searchForm = AvailabilityForm(request.POST)
        mailform = MailListForm(request.POST)
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!")
            return redirect('reservations-home')
        if searchForm.is_valid(): 
            checkInDate = searchForm.cleaned_data['checkInDate']
            checkOutDate = searchForm.cleaned_data['checkOutDate']
            inputdate = datetime.strptime(str(checkInDate), '%Y-%m-%d')
            # Perform date validation 
            if checkOutDate <= checkInDate:     #if check-out is before check-in
                messages.error(request, "Error: Check-out date must be AFTER check-in date. Please try again.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if checkInDate < date.today():  #if check-in date is in the past
                messages.error(request, "Error: Check-in date cannot be in the past. Please try again.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if (inputdate - datetime.now()).days > 365:
                messages.error(request, "We are sorry, Moffat-Bay Marina & Lodge does not accept reservations for more than a year in advance. Please come back soon to book your stay!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                guests = searchForm.cleaned_data['guests']
                checkInDate = checkInDate.strftime('%Y-%m-%d')
                checkOutDate = checkOutDate.strftime('%Y-%m-%d')
                roomID = alt_get_available_rooms(checkInDate, checkOutDate, size)
                if roomID:
                    return redirect('book-reservation', checkInDate, checkOutDate, guests, roomID)
                else:
                    messages.info(request, "We're sorry, but that room size is not available during your requested dates. Our available rooms are listed below.")
                    return redirect('available_rooms', checkInDate, checkOutDate, guests)
    else: 
        mailform = MailListForm()
        searchForm = AvailabilityForm()
        roomSize = RoomChoices.objects.filter(choiceID=size).get()
    context = {
        'title':'Select dates',
        'size': size,
        'mailform':mailform,
        'searchForm': searchForm,
        'roomSize': roomSize,
    }
    return render(request, 'reservations/book_room.html', context)

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
    
