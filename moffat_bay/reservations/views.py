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
        searchForm = AvailabilityForm(request.POST)
        mailform = MailListForm(request.POST)
        if searchForm.is_valid(): 
            checkInDate = searchForm.cleaned_data['checkInDate']
            checkOutDate = searchForm.cleaned_data['checkOutDate']
            inputdate = datetime.strptime(str(checkInDate), '%Y-%m-%d')
            # Perform date validation 
            if checkOutDate <= checkInDate:     #if check-out is before check-in
                messages.error(request, "Error: Check-out date must be AFTER check-in date. Please try again.", extra_tags='search_room')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if checkInDate < date.today():  #if check-in date is in the past
                messages.error(request, "Error: Check-in date cannot be in the past. Please try again.", extra_tags='search_room')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if (inputdate - datetime.now()).days > 365:
                messages.error(request, "We are sorry, Moffat-Bay Marina & Lodge does not accept reservations for more than a year in advance. Please come back soon to book your stay!", extra_tags='search_room')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #if no date validation errors:
            guests = searchForm.cleaned_data['guests']
            checkInDate = checkInDate.strftime('%Y-%m-%d')
            checkOutDate = checkOutDate.strftime('%Y-%m-%d')
            
            return redirect('available_rooms', checkInDate, checkOutDate, guests) 
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]
    

    context = {
        'title':'Landing Page',
        'mailform': mailform,
        'searchForm': searchForm,
        'has_mailform_messages': mail_form_messages,
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
                messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
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
                if send_contact_email(contact_data):
                    messages.success(request, "Your message has been sent!", extra_tags='contact_form')  # Display success message
                    #i tried to have it redirect to the #contact-from div here but could not determine a simple way
                    #will look into more simple options....
                else:
                    messages.error(request, "Failed to send your message. Please try again.", extra_tags='contact_form')  # Display error message
    
    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]
    
    context = {
        'title': 'Contact Us',
        'mailform': mailform,
        'contact_form': contact_form,  # Add the contact form to the context
        'has_mailform_messages': mail_form_messages,
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
                messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
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
                if send_contact_email(contact_data):
                    messages.success(request, "Your message has been sent!", extra_tags='contact_form')  # Display success message
                else:
                    messages.error(request, "Failed to send your message. Please try again.", extra_tags='contact_form')  # Display error message

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]


    context = {
        'title': 'Contact Us',
        'mailform': mailform,
        'contact_form': contact_form,  # Add the contact form to the context
        'has_mailform_messages': mail_form_messages,
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
            messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
            return redirect('attractions')
        
    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'title':'Local Attractions',
        'mailform': mailform,
        'has_mailform_messages': mail_form_messages,
        #add search availability form here
        #add anything else we want returned and displayed on about page here
        }
    return render(request, 'reservations/attractions.html', context)

#reservation lookup view:
@login_required
def reservation_lookup(request, *args, **kwargs):
    mailform = MailListForm(request.POST or None)
    mySearchForm = MyReservationSearchForm(request.POST or None)
    myReservation = None  # Initialize myReservation to None
    search_value = None

    if request.method == "POST":
        if 'mailform_submit' in request.POST:  # Check if the mailform was submitted
            if mailform.is_valid():
                mailform.save()
                messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
                return redirect('reservation_lookup')
        elif 'reservation_lookup_submit' in request.POST:  # Check if the mySearchForm was submitted
            if mySearchForm.is_valid():
                search_value = mySearchForm.cleaned_data['searchConfirm']
                # Retrieve reservation based on the search criteria (confirmation key)
                myReservation = Reservations.objects.filter(confirmationKey=search_value).first()

                if myReservation:
                    messages.success(request, "Reservation found!", extra_tags='reservation-found-result')
                else:
                    messages.error(request, "No reservation found with the provided confirmation key.", extra_tags='not-found-result')

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'title': 'My Reservations',
        'mailform': mailform,
        'has_mailform_messages': mail_form_messages,
        'mySearchForm': mySearchForm,
        'searchValue': search_value,
        'myReservation': myReservation,  # Add the myReservation to the context
    }

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
    mailform = MailListForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]


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
        'mailform': mailform,
        'has_mailform_messages': mail_form_messages,
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
                messages.error(request, "Error: Check-out date must be AFTER check-in date. Please try again.", extra_tags='search_room')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if checkInDate < date.today():  #if check-in date is in the past
                messages.error(request, "Error: Check-in date cannot be in the past. Please try again.", extra_tags='search_room')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if (inputdate - datetime.now()).days > 365:
                messages.error(request, "We are sorry, Moffat-Bay Marina & Lodge does not accept reservations for more than a year in advance. Please come back soon to book your stay!", extra_tags='search_room')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #if no date validation errors:
            guests = searchForm.cleaned_data['guests']
            checkInDate = checkInDate.strftime('%Y-%m-%d')
            checkOutDate = checkOutDate.strftime('%Y-%m-%d')
            
            return redirect('available_rooms', checkInDate, checkOutDate, guests) 
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
            return redirect('book_now')
    
    else:
        searchForm = AvailabilityForm()
        mailform = MailListForm()


    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'title':'Start your Reservation',
        'searchForm': searchForm,
        'mailform': mailform,
        'has_mailform_messages': mail_form_messages,
        }
    return render(request, 'reservations/start_booking.html', context)

def available_rooms(request, checkInDate, checkOutDate, guests):
    mailform = MailListForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'title':'Available Rooms',
        'available_rooms': get_available_rooms(checkInDate, checkOutDate),
        'guests': guests,
        'checkInDate': checkInDate,
        'checkOutDate': checkOutDate,
        'mailform': mailform,
        'has_mailform_messages': mail_form_messages,
        }
    return render(request, 'reservations/available_rooms.html', context)

# I just made some logical changes to this so that when the page is refreshed or the email form submits
# another reservation is prevented from being created if the curren one exists. 
@login_required
def booking_confirmed(request, checkInDate, checkOutDate, guests, roomID, totalCost):
    userId = request.user
    room = Rooms.objects.filter(roomID=roomID).get()

    # Check if a reservation with the same details already exists for the user
    existing_reservation = Reservations.objects.filter(
        userID=userId,
        roomID=room,
        guests=guests,
        totalPrice=totalCost,
        checkInDate=checkInDate,
        checkOutDate=checkOutDate,
    ).first()

    if existing_reservation:
        # Reservation with the same details already exists, use the existing reservation
        confirm = existing_reservation
        new_reservation_created = False
    else:
        # Generate a new confirmation key and create a new reservation
        confirmationKey = generate_confirmation_code(checkInDate, checkOutDate, guests, roomID)
        newReservation = Reservations(
            confirmationKey=confirmationKey,
            userID=userId,
            roomID=room,
            guests=guests,
            totalPrice=totalCost,
            checkInDate=checkInDate,
            checkOutDate=checkOutDate,
        )
        newReservation.save()
        confirm = Reservations.objects.filter(
            userID=userId,
            roomID=room,
            guests=guests,
            totalPrice=totalCost,
            checkInDate=checkInDate,
            checkOutDate=checkOutDate,
        ).get()
        new_reservation_created = True

    # ADD MAILLIST FORM AND HANDLING *********************************
    mailform = MailListForm(request.POST or None)
    if request.method == "POST":
        if mailform.is_valid():
            mailform.save()
            messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

     # Debugging statement to check the value of confirm.reservationID
    print("Reservation ID:", confirm.reservationID)

    context = {
        'title': 'Reservation Confirmation',
        'reservation': confirm,
        'mailform': mailform,
        'has_mailform_messages': mail_form_messages,
    }
    # Send email confirmation only if a new reservation was created
    if new_reservation_created:
        send_email_confirmation(confirm)

    return render(request, 'reservations/book_reservation_confirmation.html',context)

#alternate booking pathway:
def book_room(request, size):
    mailform = MailListForm()
    searchForm = AvailabilityForm()
    roomSize = RoomChoices.objects.filter(choiceID=size).first() 

    if request.method == "POST":
        if 'mailform_submit' in request.POST:
            mailform = MailListForm(request.POST)
            if mailform.is_valid():
                mailform.save()
                messages.success(request, "Thank you for signing up for our mailing list!", extra_tags='mail_form')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if 'filter_room_btn' in request.POST:
            searchForm = AvailabilityForm(request.POST)
            if searchForm.is_valid(): 
                checkInDate = searchForm.cleaned_data['checkInDate']
                checkOutDate = searchForm.cleaned_data['checkOutDate']
                inputdate = datetime.strptime(str(checkInDate), '%Y-%m-%d')
                # Perform date validation 
                if checkOutDate <= checkInDate:     #if check-out is before check-in
                    messages.error(request, "Error: Check-out date must be AFTER check-in date. Please try again.", extra_tags='search_room')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                if checkInDate < date.today():  #if check-in date is in the past
                    messages.error(request, "Error: Check-in date cannot be in the past. Please try again.", extra_tags='search_room')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                if (inputdate - datetime.now()).days > 365:
                    messages.error(request, "We are sorry, Moffat-Bay Marina & Lodge does not accept reservations for more than a year in advance. Please come back soon to book your stay!", extra_tags='search_room')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    guests = searchForm.cleaned_data['guests']
                    checkInDate = checkInDate.strftime('%Y-%m-%d')
                    checkOutDate = checkOutDate.strftime('%Y-%m-%d')
                    roomID = alt_get_available_rooms(checkInDate, checkOutDate, size)
                    if roomID:
                        return redirect('book-reservation', checkInDate, checkOutDate, guests, roomID)
                    else:
                        messages.info(request, "We're sorry, but that room size is not available during your requested dates. Our available rooms are listed below.", extra_tags='search_room_notfound')

    # Retrieve messages and filter 'mail_form' messages
    mail_form_messages = messages.get_messages(request)
    mail_form_messages = [message for message in mail_form_messages if 'mail_form' in message.tags]

    context = {
        'title':'Select dates',
        'size': size,
        'mailform':mailform,
        'searchForm': searchForm,
        'roomSize': roomSize,
        'has_mailform_messages': mail_form_messages,
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
    
