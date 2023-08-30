/* 
Moffat-Bay DB, tables, and triggers creation
author: Brittany Kyncl | Mark Witt
CSD-480
Mod 5.1 Assignment
8.22.23
*/

-- create database if not exists
CREATE DATABASE IF NOT EXISTS moffat_bay;
USE moffat_bay;

/* 
User table creation
User table attributes:
User_ID primary key
Email
Password
First_name
Last_name
active
staff_status
superuser
last_login
date_joined
*/
CREATE TABLE User (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(225) UNIQUE NOT NULL,
    Password VARCHAR(50) NOT NULL,
    First_name VARCHAR(50) NOT NULL,
    Last_name VARCHAR(50) NOT NULL,
    active BOOLEAN DEFAULT true,
    staff_status BOOLEAN DEFAULT false,
    superuser BOOLEAN DEFAULT false,
    last_login DATETIME DEFAULT NULL,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP
);

/* 
Custom_user table creation
Custom_user table attributes:
User primary key | foreign key references User (User_ID)
Street
City
State
Zip
Phone
Image
*/
CREATE TABLE Custom_user (
    User INT PRIMARY KEY,
    Street VARCHAR(225) DEFAULT NULL,
    City VARCHAR(50) DEFAULT NULL,
    State VARCHAR(50) DEFAULT NULL,
    Zip VARCHAR(8) NOT NULL,
    Phone VARCHAR(20) DEFAULT NULL,
    Image VARCHAR(225) DEFAULT 'default.jpg',
    FOREIGN KEY (User) REFERENCES User (User_ID)
);

/* 
Room_choices table creation
Room_choices table attributes:
choice_ID primary key
room_size
*/
CREATE TABLE Room_choices (
    choice_ID INT AUTO_INCREMENT PRIMARY KEY,
    room_size VARCHAR(50) NOT NULL
);

/* 
rooms table creation
rooms table attributes:
room_ID primary key
size foreign key references room_choices (choice_ID)
*/
CREATE TABLE rooms (
    room_ID INT AUTO_INCREMENT PRIMARY KEY,
    size INT NOT NULL,
    FOREIGN KEY (size) REFERENCES room_choices (choice_ID)
);

/* 
Stay_costs table creation
Stay_costs table attributes:
guests primary key
price 
*/
CREATE TABLE Stay_costs (
    guests INT PRIMARY KEY CHECK (guests >= 1 AND guests <= 5),
    price DECIMAL(10, 2) NOT NULL DEFAULT 120.75
);

/* 
Reservations table creation
Reservations table attributes:
reservation_id primary key
user_ID foreign key references User (User_ID)
room_ID foreign key references rooms (room_ID)
guests foreign key references Stay_costs (guests)
total_price
check_indate
checkout_date
*/
CREATE TABLE Reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    confirmation_key VARCHAR(8) UNIQUE NOT NULL,
    user_ID INT,
    room_ID INT,
    guests INT DEFAULT 1 NOT NULL CHECK (guests <= 5),
    total_price DECIMAL(10, 2) NOT NULL,
    checkin_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    FOREIGN KEY (user_ID) REFERENCES User (User_ID),
    FOREIGN KEY (room_ID) REFERENCES rooms (room_ID),
    FOREIGN KEY (guests) REFERENCES Stay_costs (guests)
);

/* 
Creat before insert trigger on 'Reservations' to calculate total_price based on rate per night 
(guest# rate) * # of nights on reservation
*/

-- create the trigger
CREATE TRIGGER calculate_total_price
BEFORE INSERT ON Reservations
FOR EACH ROW
BEGIN
    DECLARE nights INT;
    DECLARE guest_count INT;
    DECLARE nightly_price DECIMAL(10, 2);
    
    -- Calculate the number of nights between checkin_date and checkout_date
    SET nights = DATEDIFF(NEW.checkout_date, NEW.checkin_date);
    
    -- Get the number of guests from the reservation
    SELECT guests INTO guest_count FROM Stay_costs WHERE guests = NEW.guests;
    
    -- Get the nightly price for the corresponding number of guests
    SELECT price INTO nightly_price FROM Stay_costs WHERE guests = guest_count;
    
    -- Calculate the total price and update the new reservation
    SET NEW.total_price = nights * nightly_price;
END;

/* 
Creat before insert trigger on 'Reservations' to check for existing reservations
that overlap requested given dates for specific room_ID
*/

-- create the trigger
CREATE TRIGGER check_room_availability
BEFORE INSERT ON Reservations
FOR EACH ROW
BEGIN
    DECLARE room_booked INT;

    -- Check for existing reservations that overlap with the given dates
    SELECT COUNT(*) INTO room_booked
    FROM Reservations
    WHERE room_ID = NEW.room_ID
        AND NEW.checkin_date < checkout_date
        AND NEW.checkout_date > checkin_date;

    -- If there is an overlapping reservation, raise an error
    IF room_booked > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Room is already booked for the selected dates';
    END IF;
END;

/* 
Creat before insert trigger on 'Reservations' to assign randomly generated unique 8 digit confrimation key
*/
CREATE TRIGGER generate_confirmation_key
BEFORE INSERT ON Reservations
FOR EACH ROW
BEGIN
    DECLARE confirmation VARCHAR(8);
    SET confirmation = LPAD(FLOOR(RAND() * 100000000), 8, '0');
    
    -- Check if the generated confirmation number already exists
    WHILE EXISTS (SELECT 1 FROM Reservations WHERE confirmation_key = confirmation) DO
        SET confirmation = LPAD(FLOOR(RAND() * 100000000), 8, '0');
    END WHILE;
    
    SET NEW.confirmation_key = confirmation;
END;
