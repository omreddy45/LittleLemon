from django.test import TestCase
from restaurant.models import Menu, Booking
from restaurant.serializers import MenuSerializer, BookingSerializer
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime

class MenuModelTest(TestCase):
    def setUp(self):
        self.item = Menu.objects.create(
            title='Lemon Cake', price=10.99, inventory=5
        )

    def test_create_menu_item(self):
        self.assertEqual(self.item.title, 'Lemon Cake')
        self.assertEqual(float(self.item.price), 10.99)
        self.assertEqual(self.item.inventory, 5)

    def test_menu_str(self):
        self.assertEqual(str(self.item), 'Lemon Cake : 10.99')

class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            name='John Doe',
            no_of_guests=4,
            booking_date=datetime(2024, 12, 25, 18, 0)
        )

    def test_create_booking(self):
        self.assertEqual(self.booking.name, 'John Doe')
        self.assertEqual(self.booking.no_of_guests, 4)

    def test_booking_str(self):
        self.assertIn('John Doe', str(self.booking))

class MenuSerializerTest(TestCase):
    def setUp(self):
        self.item = Menu.objects.create(
            title='Greek Salad', price=12.50, inventory=8
        )
        self.serializer = MenuSerializer(instance=self.item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title', 'price', 'inventory'})

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Greek Salad')

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Menu.objects.create(title='Bruschetta', price=8.50, inventory=10)
        Menu.objects.create(title='Pasta', price=14.00, inventory=6)

    def test_get_all_menu_items(self):
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_menu_item(self):
        item = Menu.objects.first()
        response = self.client.get(f'/api/menu-items/{item.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], item.title)

class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.booking = Booking.objects.create(
            name='Alice', no_of_guests=2,
            booking_date=datetime(2024, 11, 15, 19, 0)
        )

    def test_get_all_bookings(self):
        response = self.client.get('/api/bookings/tables/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking(self):
        data = {
            'name': 'Bob',
            'no_of_guests': 3,
            'booking_date': '2024-12-20T18:00:00Z',
        }
        response = self.client.post('/api/bookings/tables/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_booking_rejected(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get('/api/bookings/tables/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
