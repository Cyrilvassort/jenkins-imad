import unittest
from app import *

class TestEmployeeAPI(unittest.TestCase):

    # Test the GET request
    def test_get(self):
        response = employees()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    # Test the POST request
    def test_post(self):
        data = {
            'firstName': 'John Doe',
            'lastName': 'engineer',
            'emailId': 'hellopodjezpinfpzeoinoinfezoijnoi'
        }
        response = employees(method="POST", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['id'])

    # Test the PUT request
    def test_put(self):
        data = {
            'firstName': 'Jane Doe',
            'lastName': 'administrator',
            'emailId': 'hello@gmail.com'
        }
        response = employees(employee_id=1, method="PUT", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Employee updated successfully')

    # Test the DELETE request
    def test_delete(self):
        response = employees(employee_id=1, method="DELETE")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Employee deleted successfully')
