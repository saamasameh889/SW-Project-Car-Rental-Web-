## Rent-A-Ride: Online Car Rental System

## Introduction

Rent-A-Ride is a full-stack web-based car rental management platform that allows users to search, book, and review cars available for rent. The system is designed for efficiency, scalability, and ease of use for both end-users and administrators.

## Features

    User registration and authentication

    Car search and filtering by brand, price, or availability

    Booking management with calendar-based interface

    User dashboard with rental history

    Admin panel for car, user, and booking management

    Review and rating system for cars

    Email notifications for bookings

    Responsive design for desktop and mobile

    Secure JWT-based session management

## Technology Stack
Frontend:

    HTML5, CSS3, JavaScript

    Bootstrap 5

Backend:

    Python 3.x

    Flask (RESTful API)

Database:

    MySQL 8.x

## Other Tools:

    SQLAlchemy ORM

    bcrypt (for password hashing)

    JWT (for authentication)

    Jinja2 (templating)

## System Architecture

    Frontend:
    Uses HTML/CSS and JavaScript for rendering dynamic and responsive user interfaces.

    Backend:
    Flask API handles routing, authentication, data manipulation, and business logic.

    Database:
    MySQL stores all data, including users, cars, bookings, and reviews.

## Installation Guide
Prerequisites:

    Python 3.x

    MySQL 8.x

    pip (Python package installer)

## Steps:

Create and Activate Virtual Environment:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Configure MySQL Database:

    Create a MySQL database named rent_a_ride

    Update config.py with your DB credentials

Initialize Database:

flask db init
flask db migrate
flask db upgrade

Run the Application:

    flask run

    Access in Browser:
    Navigate to http://localhost:5000

Usage Instructions
For Users:

    Register or log in

    Search available cars

    Book a car by selecting pickup and drop-off dates

    View and manage bookings in the dashboard

    Leave reviews and ratings

For Admins:

    Login with admin credentials

    Add/edit/remove cars

    View and manage all bookings

    Manage registered users

## Database Schema (Simplified)

    Users: user_id, name, email, password, role

    Cars: car_id, model, brand, price, location, availability

    Bookings: booking_id, user_id, car_id, start_date, end_date, status

    Reviews: review_id, user_id, car_id, rating, comment, timestamp

## Design Patterns Used
Pattern	Purpose
Singleton	Ensures single instance of DB connection
Factory	Creates car objects with shared structure
Observer	Manages event-driven notifications
Strategy	Implements flexible pricing strategies

## Testing

    Unit Testing: PyTest used for user and booking modules

    Integration Testing: Booking workflow and admin operations

    User Acceptance Testing: Conducted with feedback collection

    Performance Testing: Using Locust for concurrency simulation# Software-Project

## Screenshots
![Screenshot 2025-06-12 231823](https://github.com/user-attachments/assets/ef96f980-4b22-4bb1-9336-f0cc199127d0)

![Screenshot 2025-06-12 231901](https://github.com/user-attachments/assets/3132a981-5371-4586-b6a0-5d943887a194) 
![Screenshot 2025-06-12 231914](https://github.com/user-attachments/assets/eb276170-b69b-4a22-9291-6246a2327483) 
![Screenshot 2025-06-12 231934](https://github.com/user-attachments/assets/d98e8f0a-4347-4952-bcab-b51ac5f9960e)
![Screenshot 2025-06-12 232002](https://github.com/user-attachments/assets/ec256bc9-0e71-428c-8738-60bfd585f51b)
