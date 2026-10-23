Little Lemon Restaurant API
============================

API Paths for Testing
---------------------

Static HTML Home Page:
  /

Menu API (no auth required):
  GET    /api/menu-items/          - List all menu items
  POST   /api/menu-items/          - Create a menu item
  GET    /api/menu-items/<id>      - Retrieve a single menu item
  PUT    /api/menu-items/<id>      - Update a menu item
  DELETE /api/menu-items/<id>      - Delete a menu item

Table Booking API (auth required):
  GET    /api/bookings/tables/     - List all bookings
  POST   /api/bookings/tables/     - Create a booking
  GET    /api/bookings/tables/<id>/- Retrieve a single booking
  PUT    /api/bookings/tables/<id>/- Update a booking
  DELETE /api/bookings/tables/<id>/- Delete a booking

User Registration & Authentication:
  POST   /auth/users/              - Register a new user
  POST   /api-token-auth/          - Obtain auth token (username + password)

Setup
-----
1. cd littlelemon-capstone
2. pipenv install
3. pipenv shell
4. Create MySQL database: CREATE DATABASE reservations;
5. Update USER and PASSWORD in littlelemon/settings.py
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py createsuperuser
9. python manage.py runserver

Testing
-------
  python manage.py test
