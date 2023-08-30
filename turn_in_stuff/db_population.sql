/* 
Moffat-Bay record population
author: Brittany Kyncl | Mark Witt
CSD-480
Mod 5.1 Assignment
8.22.23
*/

-- inserting data into User Table
INSERT INTO User (Email, Password, First_name, Last_name)
VALUES ('user1@example.com', 'Password1', 'John', 'Doe'),
       ('user2@example.com', 'Password2', 'Jane', 'Smith'),
       ('user3@example.com', 'Password3', 'Sarah', 'Carson'),
       ('user4@example.com', 'Password4', 'Marcus', 'Green'),
       ('user5@example.com', 'Password5', 'Alice', 'Johnson');

-- inserting data into CustomUser table
INSERT INTO Custom_user (User, Street, City, State, Zip, Phone, Image)
VALUES (1, '123 Main St', 'Springfield', 'IL', '62701', '555-123-4567', 'user1.jpg'),
       (2, '456 Elm St', 'Los Angeles,', 'CA', '90001', '555-987-6543', 'user2.jpg'),
       (3, '789 Cherry St', 'New York', 'NY', '10001', '555-555-1234', 'user3.jpg'),
       (4, '101 Florence St', 'Miami', 'FL', '33101', '555-888-9999', 'user4.jpg'),
       (5, '112 Oak St', 'Houston', 'TX', '77001', '555-333-2222', 'user5.jpg');

-- inserting data into Room_choices table
INSERT INTO Room_choices (room_size)
VALUES ('Queen Bed'),
       ('King Bed'),
       ('Double Full Beds'),
       ('Double Queen Beds');

-- inserting data into Rooms table
INSERT INTO rooms (size)
VALUES (1), -- 1
       (1), -- 2
       (1), -- 3
       (1), -- 4
       (1), -- 5
       (1), -- 6
       (2), -- 7
       (2), -- 8
       (2), -- 9
       (2), -- 10
       (2), -- 11
       (2), -- 12
       (3), -- 13
       (3), -- 14
       (3), -- 15
       (3), -- 16
       (3), -- 17
       (3), -- 18
       (4), -- 19
       (4), -- 20
       (4), -- 21
       (4), -- 22
       (4), -- 23
       (4); -- 24

-- inserting data into  Stay_costs table
INSERT INTO Stay_costs (guests, price)
VALUES (1, 120.75),
       (2, 120.75),
       (3, 157.50),
       (4, 157.50),
       (5, 157.50);

-- inserting data into Reservations table
INSERT INTO Reservations (user_ID, room_ID, guests, checkin_date, checkout_date)
VALUES (1, 5, 2, '2023-11-08', '2023-11-13'), -- 5 nights
       (2, 8, 2, '2023-12-10', '2023-12-13'), -- 3 nights
       (3, 14, 4, '2024-01-05', '2024-01-12'), -- 7 nights
       (4, 20, 5, '2023-10-07', '2023-10-11'), -- 4 nights
       (4, 24, 2, '2024-05-03', '2024-05-06'), -- 3 nights
       (3, 1, 1, '2023-09-06', '2023-09-11'), -- 5 nights
       (3, 8, 3, '2023-10-07', '2023-10-11'), -- 4 nights
       (2, 9, 1, '2023-12-10', '2023-12-11'), -- 1 night
       (1, 6, 2, '2023-12-10', '2023-12-13'), -- 5 nights
       (5, 11, 3, '2023-10-28', '2023-11-03'); -- 6 nights 

/* Optional select querry to display reservations by user_ID and pertinent information from their reservation

SELECT Reservations.*, User.Email, Custom_user.Phone, Room_choices.room_size
FROM Reservations
JOIN User ON Reservations.user_ID = User.User_ID
JOIN Custom_user ON User.User_ID = Custom_user.User
JOIN rooms ON Reservations.room_ID = rooms.room_ID
JOIN Room_choices ON rooms.size = Room_choices.choice_ID
WHERE Reservations.user_ID = <user_id_here>;

*/