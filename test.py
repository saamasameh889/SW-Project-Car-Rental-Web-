import unittest
from app import app, mysql
from flask import session

class TestCarRentalApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Cleanup after tests
        pass

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'index.html', response.data)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login.html', response.data)

    def test_authentication_valid_user(self):
        with self.app:
            response = self.app.post('/auth', data={
                'email': 'valid_user@example.com',
                'password': 'valid_password'
            })
            self.assertEqual(response.status_code, 302)  # Redirect after login
            self.assertIn('user_id', session)

    def test_authentication_invalid_user(self):
        response = self.app.post('/auth', data={
            'email': 'invalid_user@example.com',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'No user found', response.data)

    def test_register_user(self):
        with self.app:
            response = self.app.post('/registerVerification', data={
                'full_name': 'Test User',
                'email': 'new_user@example.com',
                'password': 'password123',
                'user_type': 'User'
            })
            self.assertEqual(response.status_code, 302)
            self.assertIn('user_id', session)

    def test_view_more_cars(self):
        response = self.app.get('/view-more')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'cars.html', response.data)

    def test_add_car(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Simulate logged-in user

            response = client.post('/add_car', data={
                'carName': 'Test Car',
                'carYear': '2022',
                'fuelType': 'Gasoline',
                'pricePerDay': '100'
            })

            self.assertEqual(response.status_code, 302)

    def test_rent_car(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Simulate logged-in user

            response = client.post('/rent', data={
                'car_id': 1,
                'rental_start_date': '2024-12-22',
                'rental_end_date': '2024-12-25',
                'phone': '1234567890'
            })

            self.assertEqual(response.status_code, 302)
            self.assertIn(b'Reservation done!', response.data)

    def test_add_review(self):
        response = self.app.post('/add_review', json={
            'user_id': 1,
            'car_id': 1,
            'review_text': 'Great car!',
            'rating': 5
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Review added successfully!', response.data)

    def test_view_reviews(self):
        response = self.app.get('/reviews/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great car!', response.data)

    def test_manage_cars(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Simulate logged-in owner

            response = client.get('/manage_cars')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'manage_cars.html', response.data)

    def test_delete_car(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Simulate logged-in user

            response = client.post('/delete_item/1')
            self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
