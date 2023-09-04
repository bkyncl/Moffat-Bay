import hashlib

#confirmation code generator:
#----Generates a hashed confirmation code using checkIn, checkOut, Guests and RoomId, 
#    then also creates a check digit for verifying validity of the confirmation code.
#    Note: resulting confirmation code is a 7 digit hexadecimal number. 
#       ***may amend to include users id# later on, to also verify authenticity***
def generate_confirmation_code(check_in_date, check_out_date, guests, roomID):
    # Concatenate input parameters into a single string
    data_to_hash = f"{check_in_date}{check_out_date}{guests}{roomID}"

    # Calculate a hash of the concatenated string
    sha256_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()

    # Use the first 6 characters of the hash as the confirmation code
    confirmation_code = sha256_hash[:6]

    # Calculate a check digit based on the confirmation code
    check_digit = sum(int(digit, 16) for digit in confirmation_code) % 10

    # Append the check digit to the confirmation code
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