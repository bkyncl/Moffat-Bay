# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team



#this utilities file will hold useful methods for the reservation portion of the system
from django.db.models import Q
import hashlib
from datetime import datetime, date
from rooms.models import RoomChoices, Rooms
from django.core.mail import send_mail

#nights calculator:
def get_nights(checkInDate, CheckOutDate):
    start_date_obj = datetime.strptime(str(checkInDate), '%Y-%m-%d')
    end_date_obj = datetime.strptime(str(CheckOutDate), '%Y-%m-%d')
    return (end_date_obj - start_date_obj).days

#price calculator:
def get_final_price(costs, checkInDate, CheckOutDate, guests):
    nights = get_nights(checkInDate, CheckOutDate)
    return (nights * costs)

#confirmation code generator:
#----Generates a hashed confirmation code using checkIn, checkOut, Guests and RoomId, 
#    then also creates a check digit for verifying validity of the confirmation code.
#    Note: resulting confirmation code is a 7 digit hexadecimal number. 
#       ***may amend to include users id# later on, to also verify authenticity***
def generate_confirmation_code(check_in_date, check_out_date, guests, roomID):
    data_to_hash = f"{check_in_date}{check_out_date}{guests}{roomID}"
    sha256_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
    confirmation_code = sha256_hash[:6]
    check_digit = sum(int(digit, 16) for digit in confirmation_code) % 10
    confirmation_code += str(check_digit)
    confirmation_code = ''.join(char.upper() for char in confirmation_code)

    return confirmation_code
"""
# Example usage: 
check_in_date = "202301010"
check_out_date = "20231015"
guests = 2
roomID = 112

confirmation_code = generate_confirmation_code(check_in_date, check_out_date, guests, roomID)
print("Confirmation Code:", confirmation_code)
"""

#Confirmation code validator:
#   Takes in hexadecimal confirmation code as parameter, 
#   uses algorithm to verify if code is valid by reversing value of the check digit
#   returns a True/False if provided confirmation code is valid
def is_valid_confirmation_code(confirmation_code):
    if len(confirmation_code) != 7:
        return False  # Confirmation code must be 7 characters long (6 characters + 1 check digit)

    confirmation_digits = confirmation_code[:6]
    provided_check_digit = int(confirmation_code[-1])

    # Calculate the expected check digit based on the confirmation digits
    expected_check_digit = sum(int(digit, 16) for digit in confirmation_digits) % 10

    return expected_check_digit == provided_check_digit

"""
#example use:
if is_valid_confirmation_code(confirmation_code):
    print("Result: Valid Confirmation Code.")
else:
    print("Result: Invalid Confirmation Code.")
"""

#Room availability search:
def find_available_rooms(checkInDate, checkOutDate, overlapping_reservations):
    #stripping date format into string
    checkInDate = date.fromisoformat(str(checkInDate))
    checkOutDate = date.fromisoformat(str(checkOutDate))
    reserved_room_ids = overlapping_reservations.values_list('roomID', flat=True)
    #create list of available room object, filter by room size (get one of each), an exclude rooms already booked.
    available_rooms =[]
    room_options = RoomChoices.objects.all()
    for room_size in room_options:
        available_room = Rooms.objects.filter(size_id=room_size.roomSize).exclude(roomID__in=reserved_room_ids).first()
        if available_room:
            available_rooms.append(available_room)
    return available_rooms

#Room availability search, by size (alternate pathway):
def alt_find_available_rooms(checkInDate, checkOutDate, overlapping_reservations, size):
    #stripping date format into string
    checkInDate = date.fromisoformat(str(checkInDate))
    checkOutDate = date.fromisoformat(str(checkOutDate))
    reserved_room_ids = overlapping_reservations.values_list('roomID', flat=True)
    available_rooms = 0
    #create list of available room object, filter by room size (get one of each), an exclude rooms already booked.
    roomsize = RoomChoices.objects.filter(choiceID=size).get() # get room object from size int input
    available_room = Rooms.objects.filter(size_id=roomsize).exclude(roomID__in=reserved_room_ids).first() #get first available room of that size
    if available_room:
        available_rooms= available_room.roomID
    return available_rooms

def send_email_confirmation(reservation):
    sender = "confirmations@moffat-bay.org"
    subject = f"Your Reservation Confirmation for " + str(reservation.checkInDate) + " to " + str(reservation.checkOutDate)
    message = (f"Greetings " + reservation.userID.first_name + "!\n\n" + 
               "Your reservation for Moffat-Bay Lodge is confirmed!\n\n"  +
               "Reservation Details:\n" + 
                "Reservation Number: " + str(reservation.reservationID) + "\n" +
                "Confirmation Number: " + reservation.confirmationKey + "\n" + 
                "Check-in date: " + str(reservation.checkInDate) + "\n" +
                "Check-out date: " + str(reservation.checkOutDate) + "\n" + 
                "# of Guests: " + str(reservation.guests) + "\n" + 
                "Total Price: $" + str(reservation.totalPrice) + "\n\n" + 
                "We look forward to seeing you soon!\n\n\n" + 
                "Sincerely,\n" + 
                "Moffat-Bay Marina & Lodge"
                )
    recipient = [reservation.userID.email, ]
    send_mail(subject, message, sender, recipient, fail_silently=False)

# contact_us email form submission to save "sent" email to same folder as reservation confirmations
# Please reconfigure the structure of the email if you like this is just a basic layout
def send_contact_email(contact_data):
    sender = contact_data['email']
    subject = "Contact Form Submission"
    message = (
        f"Hello,\n\n"
        f"A new message has been submitted through the contact form on your website.\n\n"
        f"Name: {contact_data['name']}\n"
        f"Email: {contact_data['email']}\n\n"
        f"Message:\n{contact_data['message']}\n\n"
        f"Regards,\n"
        f"Moffat-Bay Marina & Lodge"
    )
    recipient = ["bravoteam@moffat-bay.org"]  # Replace with the recipient's email address

    try:
        # Attempt to send the email
        send_mail(subject, message, sender, recipient, fail_silently=False)
        return True  # Email sent successfully
    except Exception as e:
        return False  # Error occurred while sending the email