import unittest
import requests

class TestEmployeeAPI(unittest.TestCase):
    
    base_url = "http://localhost:8080/api/v1"
    
    def test_get_employees(self):
        response = requests.get(f"{self.base_url}/employees")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_add_employee(self):
        new_employee = {
            "firstName": "Jean",
            "lastName": "Lasalle",
            "emailId": "jean.lasalle@laposte.net"
        }
        response = requests.post(f"{self.base_url}/employees", json=new_employee)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
    
    def test_update_employee(self):
        updated_employee = {
            "firstName": "Jeanne",
            "lastName": "Lasalle",
            "emailId" : "jeanne.lasalle@laposte.net"
        }
        employee_id = 1
        response = requests.put(f"{self.base_url}/employees/{employee_id}", json=updated_employee)
        self.assertEqual(response.status_code, 204)
    
    def test_delete_employee(self):
        employee_id = 1
        response = requests.delete(f"{self.base_url}/employees/{employee_id}")
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    test_order = ["test_get_employees", "test_add_employee", "test_update_employee", "test_delete_employee"] # important so the delete test will work
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main(testLoader=loader, verbosity=2)
