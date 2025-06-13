CREATE DATABASE elfinal;
USE elfinal;
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(15),
    Active TINYINT DEFAULT 0
);
INSERT INTO Users (Name, Email, Password, Phone, Active)
VALUES
('Hania', 'hania@example.com', '$2a$12$kzDxNxH.OYGhZyRp2sXeZeWmKlJbFGXdtg9Afm.kuaNc9Qit5h8H6', '01012345678', 0),
('Salma', 'salma@example.com', '$2a$12$uM1V5bsTKLqJxTQC.t67Oy3YmS4YZ5hTo0mgPWr5J6B7p84T2KnwS', '01087654321', 0);

CREATE TABLE Owners (
    OwnerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(15) DEFAULT NULL,
    Address VARCHAR(255) DEFAULT NULL
);
-- Insert data into the Owners table
INSERT INTO Owners (Name, Email, Password, Phone, Address)
VALUES
('Mahmoud Abdelrahman', 'mahmoud.abdelrahman@gmail.com', 'encryptedpassword101', '0122334455', '23 Ramses St, Cairo'),
('Fatma Nabil', 'fatma.nabil@gmail.com', 'encryptedpassword202', '0102445566', '45 El Hegaz St, Giza'),
('Salah El-Din', 'salah.eldin@gmail.com', 'encryptedpassword303', '0103666777', '10 Tahrir Square, Cairo');

CREATE TABLE Cars (
    CarID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Year INT,
    Capacity INT,
    Fuel_Type VARCHAR(50),
    Mileage_Per_Litre DECIMAL(5,2),
    Transmission VARCHAR(50),
    Price_Per_Day DECIMAL(10,2),
    Photo_URL VARCHAR(255),
    OwnerID INT,
    Offers VARCHAR(255),
    New_Price DECIMAL(10,2),
    Old_Price DECIMAL(10,2),
    FOREIGN KEY (OwnerID) REFERENCES Owners(OwnerID)  -- Change this line to reference the Owners table
);

-- Insert data into the Cars table with reduced Offers
INSERT INTO Cars (Name, Year, Capacity, Fuel_Type, Mileage_Per_Litre, Transmission, Price_Per_Day, Photo_URL, OwnerID, Offers, Old_Price, New_Price)
VALUES
('Toyota RAV4', 2021, 4, 'Hybrid', 6.1, 'Automatic', 440, '../assets/images/car-1.jpg', 1, '10% off for first-time renters', 440, 396),
('BMW 3 Series', 2019, 4, 'Gasoline', 8.2, 'Automatic', 350, '../assets/images/car-2.jpg', 1, 'Weekend special: 15% off', 350, 297.5),
('Volkswagen T-Cross', 2020, 4, 'Gasoline', 5.3, 'Automatic', 400, '../assets/images/car-3.jpg', 2, NULL, NULL, NULL),
('Cadillac Escalade', 2020, 7, 'Gasoline', 7.7, 'Automatic', 620, '../assets/images/car-4.jpg', 2, NULL, NULL, NULL),
('BMW 4 Series GTI', 2021, 4, 'Gasoline', 7.6, 'Automatic', 530, '../assets/images/car-5.jpg', 3, NULL, NULL, NULL),
('BMW 4 Series', 2019, 4, 'Gasoline', 7.2, 'Automatic', 490, '../assets/images/car-6.jpg', 1, 'Holiday offer: 20% off', 490, 392),
('MG ZS', 2021, 5, 'Electric', 6.5, 'Automatic', 350, '../assets/images/car-7.jpg', 2, NULL, NULL, NULL),
('MG Hector', 2020, 5, 'Petrol', 9.0, 'Automatic', 450, '../assets/images/car-8.jpg', 3, 'Free insurance with booking', 450, 450),
('MG Gloster', 2022, 7, 'Diesel', 10.0, 'Automatic', 550, '../assets/images/car-9.jpeg', 3, NULL, NULL, NULL),
('MG Astor', 2021, 5, 'Petrol', 12.5, 'Automatic', 400, '../assets/images/car-10.jpeg', 3, 'Winter promo: 15% off', 400, 340),
('MG EZS', 2022, 5, 'Electric', 6.3, 'Automatic', 470, '../assets/images/car-11.jpeg', 3, NULL, NULL, NULL),
('Toyota RAV4', 2021, 5, 'Hybrid', 7.5, 'Automatic', 470, '../assets/images/car-12.jpeg', 1, 'New year offer: 10% off', 470, 423),
('Honda Civic', 2022, 5, 'Petrol', 8.0, 'Automatic', 400, '../assets/images/car-13.jpeg', 2, 'Book for 7 days, pay for 6', 400, 400),
('Ford Mustang', 2020, 4, 'Petrol', 10.0, 'Manual', 600, '../assets/images/car-14.jpeg', 3, NULL, NULL, NULL),
('BMW X5', 2022, 5, 'Diesel', 12.0, 'Automatic', 750, '../assets/images/car-15.jpeg', 1, NULL, NULL, NULL),
('Audi Q7', 2021, 7, 'Diesel', 9.5, 'Automatic', 850, '../assets/images/car-16.jpeg', 2, '10% off for early bookings', 850, 765),
('Mercedes-Benz G-Class', 2020, 5, 'Petrol', 8.5, 'Automatic', 1200, '../assets/images/car-17.jpeg', 3, NULL, NULL, NULL),
('Lexus RX', 2022, 5, 'Hybrid', 10.0, 'Automatic', 950, '../assets/images/car-18.jpeg', 3, NULL, NULL, NULL),
('Nissan Altima', 2023, 5, 'Petrol', 12.0, 'Automatic', 450, '../assets/images/car-19.jpeg', 2, NULL, NULL, NULL),
('Kia Seltos', 2022, 5, 'Petrol', 14.0, 'Automatic', 350, '../assets/images/car-20.jpeg', 1, NULL, NULL, NULL),
('Tesla Model 3', 2023, 5, 'Electric', 15.0, 'Automatic', 850, '../assets/images/car-21.jpeg', 2, 'Eco-friendly deal: 20% off', 850, 680);

-- Create the Rentals table
CREATE TABLE Rentals (
    RentalID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    CarID INT,
    RentalStartDate DATE,
    RentalEndDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CarID) REFERENCES Cars(CarID)
);

-- Insert sample data into Rentals table
INSERT INTO Rentals (UserID, CarID, RentalStartDate, RentalEndDate)
VALUES
(1, 1, '2024-12-01', '2024-12-10'),
(2, 2, '2024-12-05', '2024-12-15');

Select * from cars; 
SET SQL_SAFE_UPDATES = 0;
UPDATE Cars SET New_Price = 390 WHERE Name = 'Honda Civic' AND Year = 2022;
UPDATE Cars SET New_Price = 410 WHERE Name = 'MG Hector' AND Year = 2020;
SET SQL_SAFE_UPDATES = 1;


