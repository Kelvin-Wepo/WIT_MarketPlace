# WIT_MarketPlace

## Description

This Django project is designed to create a pool of women with their tech skills and
facilitate them in selling their services to potential clients and employers. It
includes user authentication, profiles, skills listings and payment methods. 

## Setup Instructions

Clone the repository.
Install the required dependencies using pip install -r requirements.txt.
Apply database migrations using python manage.py migrate.
Create a superuser using python manage.py createsuperuser.
Run the development server using python manage.py runserver.

## Usage

Access the admin panel at http://127.0.0.1:8000/admin/ and log in with
the user credentials.
Manage users, profiles, users skills and payments through the user interface.
Clients can browse users skills, select a service and provide reviews.
Users can add skills they offer service to.

## Models

### User

Custom user model with additional fields for users, clients, and reviews.

### Seller_rofile

One-to-one relationship with User model.
Contains fields for authentication information, user profile, certifications and languages.
Includes methods for saving, deleting, updating profiles, and
rating user.


### Buyer_profile

Contains fields for authentication information, user profile, certifications and languages.
Includes methods for saving, deleting, updating profiles
Methods for saving, deleting, and updating owner posts.

### Order

Contains fields for client name, email address, date,
service and user ID.
Methods for saving, deleting, updating orders, and retrieving orders
by service.


### Reviews

Contains fields for user name, email, content, rating and client ID.

## Technologies Used

Django   
AfricasTalking API


## Contributors

Kelvin Wepo 

Elizabeth Mwangi

Mercy Wairimu 

Myles Kerubo

JoyLiza Mwangi

## License

This project is licensed under the MIT License - see the
LICENSE.md file for details.